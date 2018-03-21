
import db
from error import Error

import rx.norm

class CouldNotFindBaseIngredient(Error):
    """The given name could not be resolved to a base drug"""
    status_code = 400
    error_code = 901

def perform(name):
    candidates = rx.norm.lookup_approx(name)

    if len(candidates) == 0 or candidates[0].score < 75:
        raise CouldNotFindBaseIngredient()

    cui = candidates[0].cui

    props = rx.norm.props(cui)

    actual_name = props.get("name")
    tty = props.get("tty")

    desired_type = "SBD" if tty == "BN" else "SCD"

    drugs = rx.norm.related_by_types(cui, types=[desired_type])
    print(drugs)
