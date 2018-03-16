"""
Helper methods and classes for working with RxClass, an API for finding drug relationships
and classifications
"""

import rx

def classes_raw(cui):
    """
    Returns all classes that a given RxCui belongs to, along with related concepts 
    """

    path = "/rxclass/class/byRxcui.json"
        
    resp = rx.get(path, params=dict(rxcui=cui))
    resp.raise_for_status()

    data = resp.json().get('rxclassDrugInfoList').get('rxclassDrugInfo')
    return data

def classes(cui):
    """
    Cleans up info from `classes_raw` and merges related concept info
    """
    pass
