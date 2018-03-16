"""
Helper methods and classes for working with RxNorm
"""

import rx
import collections as col

from error import Error

class MultipleIdsError(Error):
    """Multiple RxCuis exist for a given NDC"""

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

def extract_cui(data):
    ids = data.get('idGroup').get('rxnormId')

    if ids == None:
        return None

    if len(ids) > 1:
        raise MultipleIdsError()

    return ids[0]

Candidate = col.namedtuple('Candidate', ['rank', 'cui'])
def lookup_approx(term):
    """
    Performs an approximate lookup and optionally returns best result
    """
    resp = rx.get('/approximateTerm.json', params=dict(term=term))
    resp.raise_for_status()

    data = resp.json()
    candidates = data.get('approximateGroup').get('candidate')

    if len(candidates) == 0:
        return []

    rank_lookup = {}
    for candidate in candidates:
        cui = candidate.get('rxcui')
        
        if cui not in rank_lookup:
            rank = int(candidate.get('rank'))
            rank_lookup[cui] = rank

    cleaned_candidates = [Candidate(rank=rank, cui=cui)
                          for cui, rank in rank_lookup.items()]

    cleaned_candidates.sort(key=lambda canidate: canidate.rank)
    return list(map(lambda candidate: candidate.cui, cleaned_candidates))

def props(cui):
    """
    Gets associated properties for a CUI, including its type and name
    """
    path = "/rxcui/{}/properties.json".format(cui)

    data = rx.get(path, params={})
    data.raise_for_status()

    return data.json()
