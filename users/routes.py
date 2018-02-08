
from flask import Blueprint

blueprint = Blueprint('users', __name__)

@blueprint.route('/login', methods = ['GET'])
def login():
    return "YOU KNOW WHAT TIME IT IS? RIGHT?"
    

