
from flask import request, jsonify, Blueprint

import auth

blueprint = Blueprint("meds", __name__)

@blueprint.route('/add', methods = ['POST'])
@auth.required
def add():
    pass

@blueprint.route('/for-user', methods = ['POST'])
@auth.required
def for_user():
    uid = auth.uid()

    
