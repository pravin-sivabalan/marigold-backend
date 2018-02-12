
from flask import g, request
from functools import wraps

import hashlib

import jwt
import jwt.exceptions

import config_reader as conf
config = conf.read("auth")

import auth.token
import users.db

def uid():
    return g.user_id

def user():
    return users.db.find_user(uid())

def required(fn):
    """
    Wrapper for flask endpoints
    Requires the user provides valid jwt in query string
    """

    @wraps(fn)
    def decorated(*args, **kwargs):
        token = request.args.get('jwt')

        try:
            g.user_id = auth.token.user(token)
        except jwt.InvalidTokenError as err:
            return str(err)

        return fn(*args, **kwargs)

    return decorated

def calc_hash(passwd):
    hasher = hashlib.sha512()
    hasher.update(passwd.encode("utf-8"))

    return hasher.hexdigest()

