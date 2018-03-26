
from flask import g

import MySQLdb as sql
from MySQLdb.cursors import DictCursor

import db.util
import config_reader as conf

config = conf.read("database")

def make_conn():
    db_table = config["database"]
    return sql.connect(
            host = db_table["host"],
            user = db_table["user"],
            passwd = db_table["pass"],
            db = db_table["name"], 
            use_unicode=True, charset="utf8")

def conn():
    if not hasattr(g, 'db_conn'):
        g.db_conn = make_conn()

    return g.db_conn
