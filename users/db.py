
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

def create_user(first, last, email, passwd):
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

    hashed_passwd = auth.calc_hash(passwd)
    found = cursor.execute(create_user_cmd, [first, last, email, hashed_passwd])
    if found == 0:
        raise InvalidData()


    print("found: " + str(found))

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
    SELECT * from USERS
    WHERE id = %s
"""

def find_user(uid):
    conn = db.conn()
    cursor = conn.cursor()

    count = cursor.execute(find_user_with_id, [uid])
    if count == 0:
        raise InvalidUid()

    return cursor.fetchall()[0]

delete_user_with_id = """
    DELETE FROM users
    WHERE id = %s
"""

def delete_user(uid):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(delete_user_with_id, [uid])
    conn.commit()
