
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



update_allergies_cmd = """
    UPDATE users SET allergies = %s WHERE id = %s;
"""

def update_allergies(allergies, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_allergies_cmd, [allergies, id])
    conn.commit()


update_med_name_cmd = """
    UPDATE user_meds SET name = %s WHERE id = %s;
"""

def update_med_name(name, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_med_name_cmd, [name, id])
    conn.commit()


update_med_dose_cmd = """
    UPDATE user_meds SET dose = %s WHERE id = %s;
"""

def update_med_dose(dose, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_med_dose_cmd, [dose, id])
    conn.commit()


update_med_quantity_cmd = """
    UPDATE user_meds SET quantity = %s WHERE id = %s;
"""

def update_med_quantity(quantity, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_med_quantity_cmd, [quantity, id])
    conn.commit()


update_med_temporary_cmd = """
    UPDATE user_meds SET temporary = %s WHERE id = %s;
"""

def update_med_temporary(temp, id):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(update_med_temporary_cmd, [temp, id])
    conn.commit()




