import time, datetime
import MySQLdb as sql
from MySQLdb.cursors import DictCursor

import boto3
from botocore.exceptions import ClientError


def mail(email,medication_name, user_name):
    SENDER = "Marigold <mailer@marigoldapp.net>"
    RECIPIENT = email;
    AWS_REGION = "us-east-1";
    SUBJECT = "Medication Reminder"
    BODY_TEXT = ("MariGold medication reminder\r\n"
            
            )


    BODY_HTML = """<html><head><img height="100" src="https://s3.amazonaws.com/marigoldapp/MariGoldLogo.png"></head>
    <body><h2 style='font-family: "Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'>Time to take """ + medication_name + """</h2>
        <p style='font-family: "Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'>Hello """ + user_name + """, it is time to take """ + medication_name+ """.</p>
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


def mail_reminder(email,medication_name, user_name):
    SENDER = "Marigold <mailer@marigoldapp.net>"
    RECIPIENT = email;
    AWS_REGION = "us-east-1";
    SUBJECT = "Medication Reminder"
    BODY_TEXT = ("MariGold medication reminder\r\n"
            
            )


    BODY_HTML = """<html><head><img height="100" src="https://s3.amazonaws.com/marigoldapp/MariGoldLogo.png"></head>
    <body><h2 style='font-family: "Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'>""" + medication_name + """ is about to run out.</h2>
        <p style='font-family: "Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'>Hello """ + user_name + """,  """ + medication_name+ """ is about to run out. This is your reminder to refill your medication.</p>
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




get_name = """ SELECT * FROM marigold.users WHERE id = %s """

def get_user_name(id):
    cursor.execute(get_name, [id])
    user = cursor.fetchall()

    for u in user :
        return u[1], u[2], u[3]

get_med = """ SELECT * FROM marigold.user_meds WHERE id = %s """

def get_med_name(med_id):
    cursor.execute(get_med, [med_id])
    med = cursor.fetchall()

    for m in med:
        return m[3]


def make_conn():
    conn = sql.connect (host = "marigold.czubge8ebda6.us-east-1.rds.amazonaws.com",
                        user = "marigold",
                        passwd = "PQ2M4A2fdZ0wz7",
                        db = "marigold")
    return conn


conn = make_conn()
cursor = conn.cursor()

select_notification = """
    SELECT * FROM notifications;
"""

cursor.execute(select_notification)
conn.commit()

data = cursor.fetchall()

for row in data :
    id = row[0]
    user_id = row[1]
    
    medication_id = row[2]
    med_name = get_med_name(medication_id)

    day = row[3]
    time_to_take = row[4]
    
    first_name, last_name, email = get_user_name(user_id)
    user_name = first_name + " " + last_name



    now_time = datetime.datetime.now() + datetime.timedelta(minutes = 60)
    upper_bound_time = datetime.datetime.now () + datetime.timedelta(minutes = 57.6) 
    lower_bound_time = datetime.datetime.now () + datetime.timedelta(minutes = 62.4)


    if(day == datetime.datetime.today().weekday() and time_to_take.time() < lower_bound_time.time() and time_to_take.time() > upper_bound_time.time()):
        mail(email, med_name, user_name)
        print("good")
    else:
        print("bad", day, datetime.datetime.today().weekday(), lower_bound_time.time(), now_time.time(), upper_bound_time.time())




refill_notification = """ SELECT * FROM marigold.user_meds WHERE refill = 1 """

cursor.execute(refill_notification)
conn.commit()

data = cursor.fetchall()

for row in data:
    user_id = row[1]
    name = row[3]
    run_out_date = row[5]
    first_name, last_name, email = get_user_name(user_id)
    user_name = first_name + " " + last_name


    now_time = datetime.datetime.now() + datetime.timedelta(minutes = 60)
    upper_bound_time = datetime.datetime.now () + datetime.timedelta(minutes = 57.6) 
    lower_bound_time = datetime.datetime.now () + datetime.timedelta(minutes = 62.4)
    run_out_date = run_out_date #+ datetime.timedelta(minutes = 60)

    if run_out_date.weekday() == datetime.datetime.today().weekday() and run_out_date.time() < lower_bound_time.time() and run_out_date.time() > upper_bound_time.time():
        mail_reminder(email, name, user_name)
        print("mail")
    else:
        print(upper_bound_time.time(), run_out_date.time(), lower_bound_time.time())










