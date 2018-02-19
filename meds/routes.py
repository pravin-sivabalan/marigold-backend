
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
        expir_date = data["expir_date"]
    except KeyError as err:
        raise MissingDataError(err)

    meds.db.add(name, dose, expir_date)
    return jsonify(message="ok")

@blueprint.route('/for-user', methods = ['GET'])
@auth.required
def for_user():
    uid = auth.uid()

    
