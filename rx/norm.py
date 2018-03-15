"""
Helper methods and classes for working with RxNorm
"""

import rx

from error import Error

class MultipleIdsError(Error):
    """Multiple RxCuis exist for a given NDC"""

def lookup_name(name):
    """
    Returns the id associated with a drug given its's name
    """
    data = rx.get('rxcui.json', params=dict(name=name)).json()
    ids = data.get('idGroup').get('rxnormId')

    if ids == None:
        return None

    if len(ids) > 1:
        raise MultipleIdsError()

    return ids[0]

def lookup_ndc(ndc):
    """
    Returns the id associated with a drug given its's NDC code
    """
    data = rx.get('rxcui.json', params=dict(idtype="NDC", id=ndc)).json()
    ids = data.get('idGroup').get('rxnormId')

    if ids == None:
        return None

    if len(ids) > 1:
        raise MultipleIdsError()

    return ids[0]

def lookup_approx(term):
    pass

def terms(cui):
    """
    Gets associated RxTerms for a given CUI, including name, strength, and more
    """
    path = "/RxTerms/rxcui.json/{}/allinfo".format(cui)

    data = rx.get(path)
    print(data.text)
