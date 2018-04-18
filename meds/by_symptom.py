
import db
from error import Error

import rx.norm as rxn
import rx.relation as rxrel

import re
import os.path

import cache

def is_valid_drug(drug):
    name = drug["name"].lower()
    if name.count('/') > 0:
        return False

    return ("pill" in name or "oral" in name) and "powder" not in name

def clean_drug(drug):
    # Improve name if possible
    match = re.search(r'\[(.+)\]', drug["name"])
    if match is not None:
        drug["name"] = match.group(1)

    """
    loc = drug.lower().find("oral")
    if loc != -1:
        drug = drug[:loc]
    """

    drug["name"] = drug["name"].title()
    return drug

def perform(cid, rel="may_treat", limit=25):
    ingredients = rxrel.cuis_with_class(cid, rel, types=["IN"])[:limit]

    drugs = []
    for ing in ingredients:
        for drug in rxn.related_by_types(ing.cui, ["SCDF", "SBDF"]):
            drugs.append(dict(
                name = drug.name,
                cui = drug.cui,
                tty = drug.tty
            ))

    # Clean up redundancy, improve naming
    drugs = [clean_drug(drug) for drug in drugs if is_valid_drug(drug)]

    # Filter out identical drugs
    drugs.sort(key=lambda drug: drug["name"])

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

                name = classDef.name.lower()
                if "diseases" not in name and "disorders" not in name:
                    sympts.append(classDef)
            else:
                traverse(child.get(tree_key))

    traverse(tree.get(tree_key))

    sympts = list(set(sympts))
    sympts.sort(key=lambda clas: clas.name)

    cache.dump("symptoms", sympts)
