
import datetime as dt
import collections as col

import db
import auth

import rx.norm

from error import Error

import meds.fda

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

class InvalidNotification(Error):
    """Invalid notification format given"""
    status_code = 400
    error_code = 314

    def __init__(self, notification):
        self.notification = notification

add_cmd = """
    INSERT INTO user_meds (user_id, rxcui, name, quantity, run_out_date, temporary, medication_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

def next_day_of_week(date, day_of_week):
    while date.weekday() != day_of_week:
        date += dt.timedelta(days = 1)

    return date

Notification = col.namedtuple("Notification", ["day", "time"])
def parse_notification(notif):
    try:
        day = int(notif.get("day"))
        time = dt.datetime.strptime(notif.get("time"), "%Y-%m-%d:%H:%M:%S")
    except Exception as err:
        raise InvalidNotification(notif)

    return Notification(day=day, time=time)

def weekday_dist(start, end):
    dist = end - start
    if dist < 0:
        dist = 7 + dist

    return dist

def calc_run_out_date(quantity, notifications, start=None):
    if len(notifications) == 0:
        return start

    cur_dt = start if start is not None else dt.datetime.now()
    notifications = [parse_notification(notif) for notif in notifications]

    while True:
        notifications.sort(key=lambda noti: noti.time)
        notifications.sort(key=lambda noti: weekday_dist(cur_dt.day, noti.day))

        for noti in notifications:
            cur_dt = next_day_of_week(cur_dt, noti.day)
            quantity -= 1

            if quantity == 0:
                cur_dt = cur_dt.replace(hour=noti.time.hour)
                cur_dt = cur_dt.replace(minute=noti.time.minute)
                cur_dt = cur_dt.replace(second=noti.time.second)

                return cur_dt

def add(name, cui, quantity, notifications, temporary):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        quantity_parsed = int(quantity)
    except:
        raise InvalidQuantity()

    try:
        temporary_parsed = int(bool(temporary))
    except:
        raise InvalidTemporary()

    run_out_date = calc_run_out_date(quantity_parsed, notifications)

    medication_id = meds.fda.get_rx(cui)
    cursor.execute(add_cmd, [auth.uid(), cui, name, quantity_parsed, run_out_date, temporary_parsed, medication_id])

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
