
import db
import auth

from error import Error

id_field = 0
first_field = 1
last_field = 2
email_field = 3
passwd_field = 4
allergie_filed = 5



update_first_cmd = """
    UPDATE users SET first_name = %s WHERE id = %s;
"""

def update_first(first_name, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_first_cmd, [first_name, id])
    conn.commit()


update_last_cmd = """
    UPDATE users SET last_name = %s WHERE id = %s;
"""

def update_last(last_name, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_last_cmd, [last_name, id])
    conn.commit()


update_email_cmd = """
    UPDATE users SET email = %s WHERE id = %s;
"""

def update_email(email, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_email_cmd, [email, id])
    conn.commit()


update_leagues_cmd = """
    UPDATE users SET league = %s WHERE id = %s;
"""

def update_league(leagues, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_leagues_cmd, [leagues, id])
    conn.commit()

