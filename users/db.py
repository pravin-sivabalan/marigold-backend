
import db
import auth

from error import Error

id_field = 0
first_field = 1
last_field = 2
email_field = 3
passwd_field = 4

class prNotFound(Error):
    """Could not find user"""
    status_code = 400
    error_code = 20

class CredError(Error):
    pass

class InvalidPassword(CredError):
    """Password does not match database"""
    status_code = 400
    error_code = 21

class NoPasswordGiven(CredError):
    """No password was given"""
    status_code = 400
    error_code = 22


find_users_with_email = """
    SELECT * FROM users
    WHERE email = %s
"""

def check_creds(user, passwd):
    if passwd is None:
        raise NoPasswordGiven()

    conn = db.conn()
    cursor = conn.cursor()

    found = cursor.execute(find_users_with_email, [user])
    if found == 0:
        raise UserNotFound()

    user = cursor.fetchall()[0]

    hashed_passwd = auth.calc_hash(passwd)
    if user[passwd_field] != hashed_passwd:
        raise InvalidPassword()

    return user[id_field]

class UserExists(Error):
    """User already exists"""
    status_code = 409
    error_code = 23

class InvalidInput(Error):
    """Request did include correct fields"""
    status_code = 409
    error_code = 24

    def __init__(self, fields):
        self.bad_fields = fields

create_user_cmd = """
    INSERT INTO users (first_name, last_name, email, password, allergies, pharmacy_name, pharmacy_phone, pharmacy_address)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

create_user_cmd_leagues = """
    INSERT INTO users (first_name, last_name, email, password, league, allergies, pharmacy_name, pharmacy_phone, pharmacy_address)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

def create_user(first, last, email, passwd, league, allergies, pharmacy_name, pharmacy_number, pharmacy_address):
    # add validation
    invalidFields = []
    if first is None:
        invalidFields.append("first_name")
    if last is None:
        invalidFields.append("last_name")
    if email is None:
        invalidFields.append("email")
    if passwd is None:
        invalidFields.append("password")

    if len(invalidFields) != 0:
        raise InvalidInput(invalidFields)

    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    found = cursor.execute(find_users_with_email, [email])
    if found != 0:
        raise UserExists()

    hashed_password = auth.calc_hash(passwd)
    if league is None:
        found = cursor.execute(create_user_cmd, [first, last, email, hashed_password, allergies, pharmacy_name, pharmacy_number, pharmacy_address])
    else:
        found = cursor.execute(create_user_cmd_leagues, [first, last, email, hashed_password, league, allergies, pharmacy_name, pharmacy_number, pharmacy_address])
    if found == 0:
        raise InvalidData()

    id_field = cursor.lastrowid
    conn.commit()
    return id_field

class InvalidUid(Error):
    """
    The given user id was not found in the database
    """
    status_code = 500
    error_code = 23

find_user_with_id = """
    SELECT * FROM users
    WHERE id = %s
"""

def find_user(uid, custom_query=find_user_with_id):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    count = cursor.execute(custom_query, [uid])
    if count == 0:
        raise InvalidUid()

    return cursor.fetchall()[0]

def user_profile(uid):
    return find_user(uid, """
        SELECT first_name, last_name, email, league, allergies, pharmacy_name, pharmacy_address, pharmacy_phone FROM users
        WHERE id = %s
    """)

delete_user_with_id = """
    DELETE FROM users
    WHERE id = %s
"""

def delete_user(uid):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(delete_user_with_id, [uid])
    conn.commit()



def find_user_email(email):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)
    id_field = cursor.lastrowid
    conn.commit()

    count = cursor.execute(find_users_with_email, [email])
    if count == 0:
        raise UserNotFound()


    return cursor.fetchall()[0]["id"]


insert_link_string = """
    INSERT INTO reset_password (link, email, user_id)
    VALUES (%s, %s, %s);
"""


def insert_link(link, email, user_id):

    # add validation
    invalidFields = []
    if link is None:
        invalidFields.append("link")
    if email is None:
        invalidFields.append("email")
    if user_id is None:
        invalidFields.append("user_id")


    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    found = cursor.execute(insert_link_string, [link, email, user_id])
    if found == 0:
        raise InvalidData()

    conn.commit()

    return "Success"


find_users_with_link= """
    SELECT * FROM reset_password
    WHERE link = %s
"""

def find_user_by_link(link):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)
    id_field = cursor.lastrowid
    conn.commit()

    count = cursor.execute(find_users_with_link, [link])
    if count == 0:
        raise UserNotFound()


    return cursor.fetchall()[0]["user_id"]

update_password_sql = """
    UPDATE marigold.users SET password=%s WHERE id= %s
"""

def update_password(id, password):


    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)


    count = cursor.execute(update_password_sql, [password, id])
    conn.commit()

    if count == 0:
        raise UserNotFound()

    return

side_effects_cmd = """ SELECT name, possible_side_effects FROM marigold.user_meds WHERE user_id = %s """

def get_side_effects(uid):
    conn = db.conn()
    cursor = conn.cursor()
    side_effects = cursor.execute(side_effects_cmd, [uid])
    side_effects = cursor.fetchall()
    return side_effects

web_meds = """ SELECT name, id FROM marigold.user_meds WHERE user_id = %s """

def get_meds(uid):
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(web_meds, [uid])
    meds = cursor.fetchall()
    return meds







