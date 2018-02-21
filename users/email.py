import users.db

import boto3
from botocore.exceptions import ClientError

import random
import string


def change_password(email):


    random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    address = "https://marigoldapp.net/user/update-password/" + random_string;


    SENDER = "Marigold <mailer@marigoldapp.net>"
    RECIPIENT = email;
    AWS_REGION = "us-east-1";

    SUBJECT = "MariGold Password Reset"

    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )

    test = "Hello world";
    user_id = users.db.find_user_email(email)


    BODY_HTML = """<html><head><img height="100" src="https://s3.amazonaws.com/marigoldapp/MariGoldLogo.png"></head>

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

        print(random_string + " " + email + " " + str(user_id))

        users.db.insert_link(random_string, email, user_id)

        return "Success! Email sent to " + email + "<br>Link:" + random_string + "<br>User ID:" + str(user_id);




def update_password(link, password):

    id = users.db.find_user_by_link(link)
    users.db.update_password(id, password)
    print("Updated")

    return 1
