
import hashlib

import config_reader as conf

config = conf.read("auth")

def calc_hash(passwd):
    hasher = hashlib.sha512()
    hasher.update(passwd.encode("utf-8"))

    return hasher.hexdigest()
