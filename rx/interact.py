"""
Helper methods and classes for working with the NIH's Drug Interaction API
"""

import rx
import collections as col

Interaction = col.namedtuple("Interaction", ["name", "cui", "tty", "desc", "severity"])

def for_cui(cui):
    path = "/interaction/interaction.json"

    resp = rx.get(path, params=dict(rxcui=cui))
    resp.raise_for_status()

    data = resp.json().get("interactionTypeGroup")

    interactions = []
    for group in data:
        types = group.get("interactionType")

        for typ in types:
            pairs = typ.get("interactionPair")

            for pair in pairs:
                concept = pair.get("interactionConcept")
                other_drug = concept[1].get("minConceptItem")

                interactions.append(
                    Interaction(
                        name = other_drug.get("name"),
                        cui = other_drug.get("rxcui"),
                        tty = other_drug.get("tty"),
                        desc = pair.get("description"),
                        severity = pair.get("severity")
                    )
                )
    
    return interactions
