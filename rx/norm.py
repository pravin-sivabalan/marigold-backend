"""
Helper methods and classes for working with RxNorm
"""

import rx
import collections as col

from error import Error

import requests as req

class MultipleIdsError(Error):
    """Multiple RxCuis exist for a given NDC"""

def extract_cui(data):
    ids = data.get('idGroup').get('rxnormId')

    if ids == None:
        return None

    if len(ids) > 1:
        raise MultipleIdsError()

    return ids[0]

def lookup_name(name):
    """
    Returns the id associated with a drug given its's name
    """
    resp = rx.get('/rxcui.json', params=dict(name=name))
    resp.raise_for_status()

    data = resp.json()
    return extract_cui(data)

def lookup_ndc(ndc):
    """
    Returns the id associated with a drug given its's NDC code
    """
    resp = rx.get('/rxcui.json', params=dict(idtype="NDC", id=ndc))
    resp.raise_for_status()

    data = resp.json()
    return extract_cui(data)

Candidate = col.namedtuple('Candidate', ['rank', 'score', 'cui'])
def lookup_approx(term):
    """
    Performs an approximate lookup and optionally returns best result
    """
    resp = rx.get('/approximateTerm.json', params=dict(term=term))
    resp.raise_for_status()

    data = resp.json()
    candidates = data.get('approximateGroup').get('candidate')

    if candidates is None or len(candidates) == 0:
        return []

    rank_lookup = {}
    for candidate in candidates:
        cui = candidate.get('rxcui')
        
        if cui not in rank_lookup:
            rank_lookup[cui] = candidate

    cleaned_candidates = []
    for cui, candidate in rank_lookup.items():
        rank = int(candidate.get('rank'))
        score = int(candidate.get('score'))

        cleaned_candidates.append(Candidate(rank=rank, score=score, cui=cui))

    cleaned_candidates.sort(key=lambda canidate: canidate.rank)
    return cleaned_candidates

RelatedConcept = col.namedtuple("RelatedConcept", ["name", "synonym", "cui", "tty"])
def related_by_types(cui, types):
    path = "/rxcui/{}/related.json".format(cui)

    resp = rx.get(path, params=dict(tty=" ".join(types)))
    resp.raise_for_status()

    data = resp.json()

    groups = data.get("relatedGroup")
    concept_groups = groups.get("conceptGroup")

    if concept_groups is None:
        return []

    rel_concepts = []

    # Iterates over different types
    for concept_group in concept_groups:
        concept_props = concept_group.get("conceptProperties")
        if concept_props is None:
            continue

        for concept_prop in concept_props:
            rel_concepts.append(
                RelatedConcept(
                    name = concept_prop.get("name"),
                    synonym = concept_prop.get("synonym"),
                    cui = concept_prop.get("rxcui"),
                    tty = concept_prop.get("tty")
                )
            )

    return rel_concepts

def props(cui):
    """
    Gets associated properties for a CUI, including its type and name
    """
    path = "/rxcui/{}/properties.json".format(cui)

    data = rx.get(path, params={})
    data.raise_for_status()

    return data.json().get('properties')
