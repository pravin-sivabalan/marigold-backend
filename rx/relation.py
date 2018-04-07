"""
Helper methods and classes for working with RxClass, an API for finding drug relationships
and classifications
"""

import rx
import collections as col

ClassDef = col.namedtuple("ClassDef", ["name", "cid", "typ"])
def classes_of_types(types):
    """
    Returns all classes of a given type
    """
    path = "/rxclass/allClasses.json"

    resp = rx.get(path, params=dict(classTypes=" ".join(types)))
    resp.raise_for_status()

    classes = []
    concepts = resp.json().get("rxclassMinConceptList").get("rxclassMinConcept")

    for concept in concepts:
        classes.append(ClassDef(
            name = concept.get("className"),
            cid = concept.get("classId"),
            typ = concept.get("classType")
        ))
    
    return classes

Concept = col.namedtuple("Concept", ["name", "cui", "tty"])
def cuis_with_class(cid, rel=None, types=None):
    path = "/rxclass/classMembers.json"

    # TODO use different sources for relations
    params = dict(classId=cid, relaSource="NDFRT", rela=rel, trans=0)

    if types is not None:
        params["ttys"] = " ".join(types)

    resp = rx.get(path, params=params)
    resp.raise_for_status()

    data = resp.json().get("drugMemberGroup").get("drugMember")

    concepts = []
    for node in data:
        concept = node.get("minConcept")
        concepts.append(Concept(
            name = concept.get("name"),
            cui = concept.get("rxcui"),
            tty = concept.get("tty")
        ))

    return concepts

def classes_for_raw(cui):
    """
    Returns all classes that a given RxCui belongs to, along with related concepts 
    """
    path = "/rxclass/class/byRxcui.json"
        
    resp = rx.get(path, params=dict(rxcui=cui))
    resp.raise_for_status()

    data = resp.json().get('rxclassDrugInfoList').get('rxclassDrugInfo')
    return data

Class = col.namedtuple("Class", ["id", "name", "typ", "relation"])
def classes_for(cui):
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
