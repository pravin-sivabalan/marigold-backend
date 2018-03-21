
import db
from error import Error

import rx.norm
import difflib as dl

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

def jsonify(match, name_field, actual_name):
    name = getattr(match, name_field)
    diffs = [diff for diff in dl.ndiff(actual_name, name) if diff[0] != " "]

    return dict(
        name = name,
        cui = match.cui,
        diffs = len(diffs)
    )

def perform(name, limit=None):
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

    if tty == "BN":
        json_matches = [jsonify(match, name_field="synonym", actual_name=actual_name) for match in matches]
    else:
        json_matches = [jsonify(match, name_field="name", actual_name=actual_name) for match in matches]

    json_matches.sort(key=lambda drug_json: drug_json.get("name"))
    json_matches.sort(key=lambda drug_json: drug_json.get("diffs"))

    if limit is not None:
        json_matches = json_matches[:limit]

    return json_matches
