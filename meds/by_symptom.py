
import db
from error import Error

import rx.norm as rxn
import rx.relation as rxrel

import re

def is_valid_drug(drug):
    name = drug.lower()
    return ("pill" in name or "oral" in name) and "powder" not in name

def clean_drug(drug):
    # Improve name if possible
    match = re.search(r'\[(.+)\]', drug)
    if match is not None:
        drug = match.group(1)

    loc = drug.lower().find("oral")
    if loc != -1:
        drug = drug[:loc]

    return drug.title()

def perform(cid, rel="may_treat", limit=25):
    ingredients = rxrel.cuis_with_class(cid, rel, types=["IN"])[:limit]

    drugs = []
    for ing in ingredients:
        for drug in rxn.related_by_types(ing.cui, ["SCDF", "SBDF"]):
            drugs.append(drug.name)

    # Clean up redundancy, improve naming
    drugs = [clean_drug(drug) for drug in drugs if is_valid_drug(drug)]

    # Filter out identical drugs
    drugs = list(set(drugs))
    drugs.sort()

    return drugs

def generate_symptoms():
    """
    Meant to be called outside of the server, to precompute symptoms
    Its too slow to do it per request
    """
    disease_cid = rxrel.class_by_name("Disease")
    tree = rxrel.get_tree_raw(disease_cid.cid)
    tree_key = "rxclassTree"

    sympts = []
    def traverse(node):
        for child in node:
            if child.get(tree_key) is None:
                concept = child.get("rxclassMinConceptItem")
                classDef = rxrel.ClassDef(
                    name = concept.get("className"),
                    cid = concept.get("classId"),
                    typ = concept.get("classType")
                )

                if "diseases" not in classDef.name.lower():
                    sympts.append(classDef)
            else:
                traverse(child.get(tree_key))

    traverse(tree.get(tree_key))

    sympts = list(set(sympts))

    sympts.sort(key=lambda clas: clas.name)
    return sympts
