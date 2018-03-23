
import MySQLdb as sql
import hashlib

import db
import auth

tables = {}

tables["users"] = """
    CREATE TABLE `{}` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `first_name` varchar(256) NOT NULL,
        `last_name` varchar(256) NOT NULL,
        `email` varchar(256) NOT NULL,
        `password` varchar(256) NOT NULL,
        `league` varchar(256) DEFAULT NULL,
        `user_medication_ids` mediumtext,
        `banned_substance_ids` mediumtext,
        `allergies` mediumtext,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
"""

tables["user_meds"] = """
    CREATE TABLE `user_meds` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `user_id` int(11) NOT NULL,
        `medication_id` int(11) DEFAULT NULL,
        `name` mediumtext NOT NULL,
        `quantity` int(11) DEFAULT NULL,
        `run_out_date` date DEFAULT NULL,
        `temporary` int(11) DEFAULT NULL,
        `rxcui` mediumtext,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
"""

tables["meds"] = """
    CREATE TABLE `meds` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `substance_name` mediumtext,
        `adverse_reaction` mediumtext,
        `application_number` mediumtext,
        `boxed_warning` mediumtext,
        `brand_name` mediumtext,
        `drug_interactions` mediumtext,
        `generic_name` mediumtext,
        `information_for_patients` mediumtext,
        `product_type` mediumtext,
        `route` mediumtext,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
"""

def init():
    """
    Creates tables
    """
    conn = db.conn()
    cursor = conn.cursor()

    for name, cmd in tables.items():
        drop_cmd = "DROP TABLE IF EXISTS {};".format(name)

        try:
            cursor.execute(drop_cmd)
            cursor.execute(cmd.format(name))
        except sql.Error as err:
            print(err)

def add_user(first, last, email, passwd):
    conn = db.conn()
    cursor = conn.cursor()

    cmd = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES ('{}', '{}', '{}', '{}');
    """.format(first, last, email, auth.calc_hash(passwd))

    try:
        cursor.execute(cmd)
    except sql.Error as err:
        print(err)

    conn.commit()
    
