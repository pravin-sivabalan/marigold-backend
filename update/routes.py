from flask import request, jsonify, Blueprint, render_template, request

import auth
import auth.token


import boto3
from botocore.exceptions import ClientError

blueprint = Blueprint('update', __name__)

@blueprint.route('', methods = ['GET'])
@auth.required
def profile():
    return jsonify(
        message="ok",
        profile=users.db.user_profile(auth.uid())
    )

@blueprint.route('/med', methods = ['POST'])
def login():
    return "Hello World"

@blueprint.route('/profile', methods = ['POST'])
@auth.required
def test():
    output = str(auth.uid())
    return output


