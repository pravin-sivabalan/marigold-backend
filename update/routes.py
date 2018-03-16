from flask import request, jsonify, Blueprint, render_template, request

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


    return jsonify(message="ok")


