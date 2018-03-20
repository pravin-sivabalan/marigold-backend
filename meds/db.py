
import datetime as dt

import db
import auth

import rx.norm

from error import Error

id_field = 0
name_field = 1
dose_field = 2
expir_date = 3

class InvalidDate(Error):
    """Dose is not a parsable integer"""
    status_code = 400
    error_code = 31

class InvalidQuantity(Error):
    """Quantity is not a parsable integer"""
    status_code = 400
    error_code = 311

class InvalidPerWeek(Error):
    """Quantity is not a parsable integer"""
    status_code = 400
    error_code = 312

class InvalidTemporary(Error):
    """Temporary is not a parsable boolean"""
    status_code = 400
    error_code = 313

class UnknownMed(Error):
    """Specified medication has no equivalent in the NIH database"""
    status_code = 400
    error_code = 313

add_cmd = """
    INSERT INTO user_meds (user_id, rxcui, name, quantity, run_out_date, temporary)
    VALUES (%s, %s, %s, %s, %s, %s);
"""

def add(name, quantity, per_week, temporary):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        quantity_parsed = int(quantity)
    except:
        raise InvalidQuantity()

    try:
        per_week_parsed = int(per_week)
    except:
        raise InvalidPerWeek()

    try:
        temporary_parsed = int(bool(temporary))
    except:
        raise InvalidTemporary()

    weeks = int(quantity_parsed / per_week_parsed)
    run_out_date = dt.date.today() + dt.timedelta(weeks=weeks)

    candidates = rx.norm.lookup_approx(name)
    if len(candidates) == 0 or candidates[0].score < 75:
        raise UnknownMed()

    cui = candidates[0].cui 

    cursor.execute(add_cmd, [auth.uid(), cui, name, quantity_parsed, run_out_date, int(temporary_parsed)])
    conn.commit()

for_user_cmd = """
    SELECT id, medication_id, rxcui, name, quantity, run_out_date, temporary FROM user_meds
    WHERE user_id = %s
"""

def for_user():
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)
    
    cursor.execute(for_user_cmd, [auth.uid()])
    users_meds = cursor.fetchall()
   
    return users_meds

class MedIdNotFound(Error):
    """Given medicine ID was not in the database"""
    status_code = 400
    error_code = 32

delete_cmd = """
   DELETE FROM user_meds
   WHERE id = %s
"""

def delete(med_id):
    conn = db.conn()
    cursor = conn.cursor()

    count = cursor.execute(delete_cmd, [med_id])
    if count == 0:
        raise MedIdNotFound()

    conn.commit()
