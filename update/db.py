
import db
import auth

from error import Error

id_field = 0
first_field = 1
last_field = 2
email_field = 3
passwd_field = 4

class UserNotFound(Error):
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
    INSERT INTO users (first_name, last_name, email, password)
    VALUES (%s, %s, %s, %s);
"""

create_user_cmd_leagues = """
    INSERT INTO users (first_name, last_name, email, password, league)
    VALUES (%s, %s, %s, %s, %s);
"""


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


