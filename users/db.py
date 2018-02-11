
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

def check_creds(user, passwd):
    if passwd is None:
        raise NoPasswordGiven()

    
