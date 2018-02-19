from flask import Flask, render_template, request
import click

import subprocess

import users.routes
import meds.routes

import db
import db.util


import boto3
from botocore.exceptions import ClientError

from error import Error, response_for_error

app = Flask(__name__)
app.register_blueprint(users.routes.blueprint, url_prefix='/user')
app.register_blueprint(meds.routes.blueprint, url_prefix='/meds')

@app.errorhandler(Error)
def handle_error(error):
    return response_for_error(error)

# Test routes
@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
	return render_template('hello.html', name=name)

@app.route('/update/git', methods = ['GET', 'POST'])
def update():
	cmd = ["./hook.sh", ]
	return "hi"

@app.route('/database/connectiontest')
def connectiokn_test():
        config = db.config.read()
        output = "User: " + config['database']['user'] + "<br>Host: " + config['database']['host'] 
        
        return output



@app.route('/database/emailtest/<email>')
def email_test(email):

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
        return email;





# Command Line Utils
# NOT ACCESSIBLE BY WEB, DONT WORRY
# Use like so on terminal: `flask $CMD_NAME_HERE $ARG1 $ARG2 ... $ARGN

@app.cli.command("init-db")
def db_init(*args, **kwargs):
    db.util.init(*args, **kwargs)

@app.cli.command("add-user")
@click.option("--first", default="FIRST")
@click.option("--last", default="LAST")
@click.option("--email", default="EMAIL")
@click.option("--passwd", default="PASSWD")
def db_add_user(first, last, email, passwd):
    db.util.add_user(first, last, email, passwd)

if __name__ == '__main__':
  app.run(debug=True)
