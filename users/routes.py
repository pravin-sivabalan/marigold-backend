
from flask import request, Blueprint

import auth
import users.db

import json

blueprint = Blueprint('users', __name__)

@blueprint.route('/login/<user>', methods = ['GET'])
def login(user):
    passwd = request.args.get('passwd')

    try:
        user_id = users.db.check_creds(user, passwd)
    except users.db.CredError as err:
        return err.message

    return "NO"
    
@blueprint.route('/logout/<user>', methods = ['GET'])
def logut(user):
    pass

@blueprint.route('/create/<user>', methods = ['POST'])
def create(user):
    pass

@blueprint.route('/delete/<user>', methods = ['POST'])
def delete(user):
    pass

@blueprint.route('/change-password/<user>', methods = ['POST'])
def change_password(user):
    pass
