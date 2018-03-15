
from flask import request, jsonify, Blueprint

import auth
from error import Error, MissingDataError

import meds.db

blueprint = Blueprint("meds", __name__)

@blueprint.route('/add', methods = ['POST'])
@auth.required
def add():
    data = request.get_json()
        
    try:
        name = data["name"]
        dose = data["dose"]
        quantity = data["quantity"]
        per_week = data["per_week"]
        temporary = data["temporary"]
    except KeyError as err:
        raise MissingDataError(err)

    meds.db.add(name, dose, quantity, per_week, temporary)
    return jsonify(message="ok")

@blueprint.route('/for-user', methods = ['GET'])
@auth.required
def for_user():
    users_meds = meds.db.for_user()
    return jsonify(message="ok", meds=users_meds)

@blueprint.route('/delete', methods = ['POST'])
@auth.required
def delete():
    data = request.get_json()

    try:
        med_id = data["id"]
    except KeyError as err:
        raise MissingDataError(err)

    meds.db.delete(med_id)
    return jsonify(message="ok")
