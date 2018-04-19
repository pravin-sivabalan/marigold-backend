from flask import request, jsonify, Blueprint, render_template, request, redirect

import auth
import auth.token
import update.db

from error import Error, MissingDataError

blueprint = Blueprint('update', __name__)

@blueprint.route('', methods = ['GET'])
@auth.required
def profile():
    return jsonify(
        message="ok",
        profile=users.db.user_profile(auth.uid())
    )



@blueprint.route('/profile', methods = ['POST'])
@auth.required
def update_profile():
    user_id = auth.uid()
    data = request.get_json()

    if(data.get('first_name')):
        update.db.update_first(data.get('first_name'), user_id)

    if(data.get('last_name')):
        update.db.update_last(data.get('last_name'), user_id)

    if(data.get('email')):
        update.db.update_email(data.get('email'), user_id)

    if(data.get('league')):
        update.db.update_league(data.get('league'), user_id)

    if(data.get('allergies')):
        update.db.update_allergies(data.get('allergies'), user_id)


    return jsonify(message="ok")


@blueprint.route('/med', methods = ['POST'])
@auth.required
def update_med():
    user_id = auth.uid()
    data = request.get_json()

    try:
        med_id = data["med_id"]
    except KeyError as err:
        raise MissingDataError(err)

    if(data.get('name')):
        update.db.update_med_name(data.get('name'), med_id)

    if(data.get('quantity')):
        update.db.update_med_quantity(data.get('quantity'), med_id)

    if(data.get('temporary')):
        update.db.update_med_temporary(data.get('temporary'), med_id)


    return jsonify(message="ok")

