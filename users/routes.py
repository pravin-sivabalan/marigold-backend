
from flask import request, jsonify, Blueprint

import auth
import auth.token

import users.db

blueprint = Blueprint('users', __name__)

@blueprint.route('/login/<user>', methods = ['POST'])
def login(user):
    data = request.get_json()
    passwd = data.get('passwd')

    user_id = users.db.check_creds(user, passwd)
    return jsonify({
        "jwt": auth.token.create(user_id).decode("utf-8")
    })

@blueprint.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    passwd = data.get('passwd')

    user_id = users.db.create_user(first_name, last_name, email, passwd)
    return jsonify({
        "jwt": auth.token.create(user_id).decode("utf-8")
    })

@blueprint.route('/logout', methods = ['GET'])
@auth.required
def logout():
    return "Hello there: {}".format(auth.user())

@blueprint.route('/create/<user>', methods = ['POST'])
def create(user):
    pass

@blueprint.route('/delete', methods = ['POST'])
@auth.required
def delete():
    users.db.delete_user(auth.uid())
    return "Goodbye!"

@blueprint.route('/change-password', methods = ['POST'])
def change_password():
    pass
