"""
Helper methods and classes for working with RxClass, an API for finding drug relationships
and classifications
"""

import rx
import collections as col

def classes_raw(cui):
    """
    Returns all classes that a given RxCui belongs to, along with related concepts 
    """
    path = "/rxclass/class/byRxcui.json"
        
    resp = rx.get(path, params=dict(rxcui=cui))
    resp.raise_for_status()

    data = resp.json().get('rxclassDrugInfoList').get('rxclassDrugInfo')
    return data


Class = col.namedtuple("Class", ["id", "name", "typ", "relation"])

def classes(cui):
    """
    Cleans up info from `classes_raw` and merges related concept info
    Returns two arrays, the first are classes that are related by ingredient, the second are classes related by products that use the specified cui
    """
    raw_data = classes_raw(cui)

    related_by_in = set()
    related_by_prod = set()

    for raw_relation in raw_data:
        concept = raw_relation.get("minConcept")
        class_concept = raw_relation.get("rxclassMinConceptItem")
        
        rel_type = raw_relation.get("rela")
        if rel_type == "":
            rel_type = None

        class_ = Class(
            id = class_concept.get("classId"),
            name = class_concept.get("className"),
            typ = class_concept.get("classType"),
            relation = rel_type,
        )

        if concept.get("tty").endswith("IN"):
            related_by_in.add(class_)
        else:
            related_by_prod.add(class_)

    return related_by_in, related_by_prod
