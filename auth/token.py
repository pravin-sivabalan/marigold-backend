
import datetime as dt
from datetime import datetime

import jwt

import auth
from error import Error

secret = auth.config["jwt"]["secret"]
algo = auth.config["jwt"]["algo"]

token_lifetime = int(auth.config["jwt"]["lifetime"])
def create(user_id):
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + dt.timedelta(hours=token_lifetime)
    }

    return jwt.encode(payload, secret, algorithm=algo)

class JWTError(Error):
    """
    Invalid JWT provided 
    """
    status_code = 401
    error_code = 0

    def __init__(self, jwt_err):
        self.jwt_error_name = type(jwt_err).__name__


def user(token):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except jwt.InvalidTokenError as err:
        raise JWTError(err)

    return int(payload["sub"])
