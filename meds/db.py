
from datetime import datetime

import db
import auth

from error import Error

id_field = 0
name_field = 1
dose_field = 2
expir_date = 3

add_cmd = """
    INSERT INTO meds (name, dose, expir_date)
    VALUES (%s, %s, %s);
"""

class InvalidDose(Error):
    """Dose is not a parsable integer"""
    status_code = 400
    error_code = 30

class InvalidDate(Error):
    """Dose is not a parsable integer"""
    status_code = 400
    error_code = 31

def add(name, dose, expir_date):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        dose_parsed = int(dose)
    except:
        raise InvalidDose()

    try:
        expir_parsed = datetime.strptime(expir_date, '%m %d %Y')
    except:
        raise InvalidDate()

    cursor.execute(add_cmd, [name, dose_parsed, expir_parsed])
    conn.commit()
