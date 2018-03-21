
import db
from error import Error

import rx.norm

accepted_routes = ["oral", "chewable", "tablet", "capsule"]

class CouldNotFindBaseIngredient(Error):
    """The given name could not be resolved to a base drug"""
    status_code = 400
    error_code = 901

def is_mouth_drug(drug):
    for route in accepted_routes:
        if route in drug.name.lower() or route in drug.synonym.lower():
            return True

    return False

def contains_name(actual_name, drug):
    name = actual_name.lower()
    return name in drug.name.lower() or name in drug.synonym.lower()

def jsonify(match, name_field):
    return dict(
        name = getattr(match, name_field),
        cui = match.cui
    )

def perform(name, limit=10):
    candidates = rx.norm.lookup_approx(name)

    if len(candidates) == 0 or candidates[0].score < 75:
        raise CouldNotFindBaseIngredient()

    cui = candidates[0].cui

    props = rx.norm.props(cui)

    actual_name = props.get("name")
    tty = props.get("tty")

    desired_type = "SBD" if tty == "BN" else "SCD"

    drugs = rx.norm.related_by_types(cui, types=[desired_type])
    matches = [drug for drug in drugs 
                if is_mouth_drug(drug) and contains_name(actual_name, drug)]

    matches.sort(key=lambda drug: drug.name)

    if tty == "BN":
        return [jsonify(match, name_field="synonym") for match in matches]
    else:
        return [jsonify(match, name_field="name") for match in matches]
