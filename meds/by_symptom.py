
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
