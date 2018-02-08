
from flask import Blueprint

blueprint = Blueprint('users', __name__)

@blueprint.route('/login/<user>', methods = ['GET'])
def login(user):
    return "YOU KNOW WHAT TIME IT IS? RIGHT?"
    
@blueprint.route('/logout/<user>', methods = ['GET'])
def logut(user):
    pass

@blueprint.route('/create/<user>', methods = ['POST'])
def create(user):
    pass


