"""
Helper methods and classes for working with the NIH's Drug Interaction API
"""

import rx
import collections as col

InteractionForCui = col.namedtuple("InteractionForCui", ["name", "cui", "tty", "desc", "severity"])

def for_cui(cui):
    """
    Gets all interactions with a given drug
    """
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
                    InteractionForCui(
                        name = other_drug.get("name"),
                        cui = other_drug.get("rxcui"),
                        tty = other_drug.get("tty"),
                        desc = pair.get("description"),
                        severity = pair.get("severity")
                    )
                )
    
    return interactions

InteractionDrugInfo = col.namedtuple("InteractionDrugInfo", ["name", "tty", "cui"])
InteractionInfo = col.namedtuple("InteractionInfo", ["desc", "severity"])
InteractionInList = col.namedtuple("InteractionInList", ["drug1", "drug2", "info"])

def with_list(cuis):
    """
    Gets all interactions between drugs in the list `cuis`
    """
    path = "/interaction/list.json"

    resp = rx.get(path, params=dict(rxcuis=" ".join(cuis)))
    resp.raise_for_status()

    data = resp.json().get("fullInteractionTypeGroup")

    interactions = []
    for group in data:
        types = group.get("fullInteractionType")

        for typ in types:
            concepts = typ.get("minConcept")

            drug1 = InteractionDrugInfo(
                name = concepts[0].get("name"),
                tty = concepts[0].get("tty"),
                cui = concepts[0].get("rxcui")
            )

            drug2 = InteractionDrugInfo(
                name = concepts[1].get("name"),
                tty = concepts[1].get("tty"),
                cui = concepts[1].get("rxcui")
            )

            pairs = typ.get("interactionPair")
            for pair in pairs:
                interactions.append(
                    InteractionInList(
                        drug1 = drug1,
                        drug2 = drug2,
                        info = InteractionInfo(
                            desc = pair.get("description"),
                            severity = pair.get("severity")
                        )
                    )
                )

    # Now, merge interactions between the same two drugs into grouped lists
    merged_interactions = col.defaultdict(list)
    for inter in interactions:
        pair = [inter.drug1, inter.drug2]
        pair.sort(key=lambda drug: drug.cui)

        merged_interactions[tuple(pair)].append(inter.info)
    
    return merged_interactions
