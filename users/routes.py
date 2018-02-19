
from flask import request, jsonify, Blueprint

import auth
import auth.token

import users.db

import boto3
from botocore.exceptions import ClientError

blueprint = Blueprint('users', __name__)

@blueprint.route('/login/<user>', methods = ['POST'])
def login(user):
    data = request.get_json()
    passwd = data.get('passwd')

    user_id = users.db.check_creds(user, passwd)

    return jsonify(
        message="ok",
        jwt=auth.token.create(user_id).decode("utf-8")
    )

@blueprint.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    user_id = users.db.create_user(first_name, last_name, email, password)
    return jsonify(
        message="ok",
        jwt=auth.token.create(user_id).decode("utf-8")
    )

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
    return jsonify(message="ok")


@blueprint.route('/change-password/<email>')
def change_password(email):

    SENDER = "Marigold <mailer@marigoldapp.net>"
    RECIPIENT = email;
    AWS_REGION = "us-east-1";

    SUBJECT = "MariGold Password Reset"

    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )

    test = "Hello world";
    address = "google.com";


    BODY_HTML = """<html><head><img src="https://www.apple.com/favicon.ico"></head>

    <body><h2 style='font-family: "Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'>You have requested to reset your password for MariGold.</h2>

        <p style='font-family: "Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'>Please click <a href='""" + address + """'>here</a> or go to """ + address + """ to reset your password.</p>
    </body>
    </html>"""


    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )

    except ClientError as e:
        return e.response['Error']['Message'];
    else:
        return "Success! Email sent to " + email;




