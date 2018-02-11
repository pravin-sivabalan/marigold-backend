
import MySQLdb as sql

import db

def init():
    """
    Creates tables
    """
    conn = db.conn()

    print(conn) 
