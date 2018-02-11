
import datetime as dt
from datetime import datetime

import jwt

import auth

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

def user(token):
    payload = jwt.decode(token, secret, algorithms=algo)
    return int(payload["sub"])
