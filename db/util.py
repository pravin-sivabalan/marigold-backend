
import MySQLdb as sql

import db

TABLES = {}

TABLES["users"] = """
    CREATE TABLE users (
        id int(11) NOT NULL AUTO_INCREMENT,
        first_name varchar(256) NOT NULL,
        last_name varchar(256) NOT NULL,

        email varchar(256) NOT NULL,
        password varchar(256) NOT NULL,

        PRIMARY KEY(id)
    );
"""

def init():
    """
    Creates tables
    """
    conn = db.conn()
    cursor = conn.cursor()

    for name, cmd in TABLES.items():
        drop_cmd = "DROP TABLE IF EXISTS {};".format(name)

        try:
            cursor.execute(drop_cmd)
            cursor.execute(cmd)
        except sql.Error as err:
            print(err)

def add_user(first, last, email, passwd):
    conn = db.conn()
    cursor = conn.cursor()

    cmd = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES ('{}', '{}', '{}', '{}');
    """.format(first, last, email, passwd)

    try:
        cursor.execute(cmd)
    except sql.Error as err:
        print(err)

    conn.commit()
