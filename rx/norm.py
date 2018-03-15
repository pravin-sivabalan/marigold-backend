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

Candidate = col.namedtuple('Candidate', ['score', 'cui'])
def lookup_approx(term):
    pass

def terms(cui):
    """
    Gets associated RxTerms for a given CUI, including name, strength, and more
    """
    path = "/RxTerms/rxcui.json/{}/allinfo".format(cui)

    data = rx.get(path)
    print(data.text)
