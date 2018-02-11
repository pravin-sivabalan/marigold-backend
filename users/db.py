
import db
import auth

class CredError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotFound(CredError):
    """Could not find user"""
    def __init__(self):
        super().__init__(self.__doc__)

class InvalidPassword(CredError):
    """Password does not match database"""
    def __init__(self):
        super().__init__(self.__doc__)

class NoPasswordGiven(CredError):
    """No password was given"""
    def __init__(self):
        super().__init__(self.__doc__)

find_users_with_email = """
    SELECT * FROM users
    WHERE email = %s
"""

id_field = 0
first_field = 1
last_field = 2
email_field = 3
passwd_field = 4

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
