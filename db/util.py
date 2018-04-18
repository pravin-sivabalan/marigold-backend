import MySQLdb as sql
import hashlib

import db
import auth

tables = {}

tables["users"] = """
    CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(256) NOT NULL,
  `last_name` varchar(256) NOT NULL,
  `email` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `league` varchar(256) DEFAULT NULL,
  `user_medication_ids` longtext,
  `banned_substance_ids` longtext,
  `allergies` longtext,
  `pharmacy_name` mediumtext,
  `pharmacy_address` mediumtext,
  `pharmacy_phone` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
"""

tables["user_meds"] = """
    CREATE TABLE `user_meds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `medication_id` int(11) DEFAULT '-1',
  `name` mediumtext NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `run_out_date` datetime DEFAULT NULL,
  `temporary` int(11) DEFAULT NULL,
  `rxcui` mediumtext,
  `banned` mediumtext,
  `refill` int(11) DEFAULT NULL,
  `possible_side_effects` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
"""

tables["meds"] = """
    CREATE TABLE `meds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rxcui` mediumtext,
  `purpose` mediumtext,
  `inactive_ingredient` mediumtext,
  `warnings` mediumtext,
  `questions` mediumtext,
  `when_using` mediumtext,
  `generic_name` mediumtext,
  `indications_and_usage` mediumtext,
  `information_for_patients` mediumtext,
  `brand_name` mediumtext,
  `route` mediumtext,
  `warnings_and_cautions` mediumtext,
  `banned` mediumtext,
  `possible_side_effects` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
"""

tables["notifications"] = """
    CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `medication_id` int(11) NOT NULL,
  `day_to_take` int(11) NOT NULL,
  `time_to_take` datetime NOT NULL,
  `run_out_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=305 DEFAULT CHARSET=latin1
"""

tables["banned"] = """
CREATE TABLE `banned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `league` varchar(45) NOT NULL,
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=476 DEFAULT CHARSET=utf8
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


tables_to_clear = [
    "users",
    "user_meds",
    "meds",
    "notifications"
] 

def clear():
    conn = db.conn()
    cursor = conn.cursor()

    for table in tables_to_clear:
        cursor.execute("TRUNCATE TABLE {};".format(table))

    conn.commit()

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
    
