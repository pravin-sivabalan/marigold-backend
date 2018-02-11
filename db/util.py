
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
        try:
            drop_cmd = "DROP TABLE IF EXISTS {};".format(name)

            cursor.execute(drop_cmd)
            cursor.execute(cmd)
        except sql.Error as err:
            print(err)

