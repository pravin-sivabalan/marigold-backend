
import datetime as dt
from datetime import datetime

import jwt

import auth

secret = auth.config["jwt"]["secret"]

token_lifetime = 5
def create(user_id):
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp", datetime.utcnow() + dt.timedelta(hours=token_lifetime)
    }


def decode(token):
    pass
