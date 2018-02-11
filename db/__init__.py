
from flask import g
import MySQLdb as sql

import db.util
import db.config

def make_conn():
    config  = db.config.read()

    db_table = config["database"]
    return sql.connect(
            host = db_table["host"],
            user = db_table["user"],
            passwd = db_table["pass"],
            db = "marigold")

def conn():
    if not hasattr(g, 'db_conn'):
        g.db_conn = db.util.make_conn()

    return g.db_conn
