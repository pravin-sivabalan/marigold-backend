
from flask import g
import MySQLdb as sql

import db.util
import config_reader as conf

config = conf.read("database")

class Error(Exception):
    def __init__(self, message):
        self.message = message

def make_conn():
    db_table = config["database"]
    return sql.connect(
            host = db_table["host"],
            user = db_table["user"],
            passwd = db_table["pass"],
            db = db_table["name"])

def conn():
    if not hasattr(g, 'db_conn'):
        g.db_conn = make_conn()

    return g.db_conn
