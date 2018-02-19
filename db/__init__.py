
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
            db = db_table["name"])

def conn():
    if not hasattr(g, 'db_conn'):
        g.db_conn = make_conn()

    return g.db_conn

def fetch_dict(cursor, n=None):
    """
    After executing a query, this method will fetch all results and then convert them to an array of dictionaries
    Handy for outputing results into JSON
    """
    result = []
    
    query_result = cursor.fetchall() if n is None else cursor.fetchmany(n)
    

    return result
