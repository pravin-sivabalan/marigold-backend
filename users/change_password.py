import boto3
from botocore.exceptions import ClientError

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


    BODY_HTML = """<html><head><img src="https://s3.amazonaws.com/marigoldapp/MariGoldLogo.png" width="500"></head>

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


