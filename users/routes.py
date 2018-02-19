
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


@blueprint.route('/change-password/<email>')
def change_password(email):

    SENDER = "Marigold <mailer@marigoldapp.net>"
    RECIPIENT = email;
    AWS_REGION = "us-east-1";

    SUBJECT = "Amazon SES Test (SDK for Python)"

    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )

    test = "Hello world"


    BODY_HTML = """<html><head></head><body><h1>Amazon SES Test (SDK for Python) """ + test + """</h1><p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
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




