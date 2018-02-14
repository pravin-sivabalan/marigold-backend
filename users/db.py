
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
    error_code = 0

class CredError(Error):
    pass

class InvalidPassword(CredError):
    """Password does not match database"""
    status_code = 400
    error_code = 1

class NoPasswordGiven(CredError):
    """No password was given"""
    status_code = 400
    error_code = 2

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

class InvalidUid(Error):
    """
    The given user id was not found in the database
    """

find_user_with_id = """
    SELECT * from USERS
    WHERE id = %d
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

