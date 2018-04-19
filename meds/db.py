
import datetime as dt
import collections as col

import db
import auth

import rx.norm

from error import Error

import meds.fda
import notification.db

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

class InvalidAlertUser(Error):
    """Alert_user is not a parsable boolean"""
    status_code = 400
    error_code = 314

class InvalidNotification(Error):
    """Invalid notification format given"""
    status_code = 400
    error_code = 315

    def __init__(self, notification):
        self.notification = notification

add_cmd = """
    INSERT INTO user_meds (user_id, rxcui, name, quantity, run_out_date, temporary, medication_id, banned, possible_side_effects, refill)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

select_cmd = """
    SELECT id FROM  user_meds  WHERE user_id = '%s' AND rxcui = %s AND name = %s AND quantity = '%s' AND run_out_date = %s AND temporary = '%s' AND medication_id = '%s';
"""

def next_day_of_week(date, noti):
    if date.weekday() == noti.day:
        temp_date = date.replace(year=noti.time.year, month=noti.time.month, day=noti.time.day)

        if temp_date >= noti.time:
            date += dt.timedelta(days = 1)

    while date.weekday() != noti.day:
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

def calc_run_out_date(quantity, notifications, start):
    cur_dt = start
    if len(notifications) == 0:
        return start

    while True:
        notifications.sort(key=lambda noti: noti.time)
        notifications.sort(key=lambda noti: weekday_dist(cur_dt.day, noti.day))

        for noti in notifications:
            cur_dt = next_day_of_week(cur_dt, noti)
            quantity -= 1

            if quantity == 0:
                cur_dt = cur_dt.replace(hour=noti.time.hour)
                cur_dt = cur_dt.replace(minute=noti.time.minute)
                cur_dt = cur_dt.replace(second=noti.time.second)

                return cur_dt

def get_leagues_banned_in(name):

    conn = db.conn()
    cursor = conn.cursor()
    banned_cmd = """SELECT league FROM banned WHERE name like %s"""
    cursor.execute(banned_cmd, [name.split(' ',1)[0]])
    leagues = cursor.fetchall()
    league_banned = ""

    for l in leagues:
        league_banned += l[0] + ','


    return league_banned[:-1]



def add(name, cui, quantity, notifications, temporary, alert_user, refill):
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

    try:
        alert_user_parsed = bool(alert_user)
    except:
        raise InvalidAlertUser()

    notifications = [parse_notification(notif) for notif in notifications]
    run_out_date = calc_run_out_date(quantity_parsed, notifications, start=dt.datetime.now())

    medication_id = meds.fda.get_rx(cui)
    side_effects = get_drug_side_effects(cui)

    leagues_banned_in = get_leagues_banned_in(name)

    cursor.execute(add_cmd, [auth.uid(), cui, name, quantity_parsed, run_out_date.strftime('%Y-%m-%d %H:%M:%S'), temporary_parsed, medication_id, leagues_banned_in, side_effects, refill])

    cursor.execute("SELECT LAST_INSERT_ID();")
    get_id = cursor.fetchall()


    medication_notification_id = get_id[0][0]


    conn.commit()

    if alert_user:
        for notif in notifications:
            #print(medication_notification_id, notif.day, notif.time, run_out_date.strftime('%Y-%m-%d %H:%M:%S'))
            notification.db.add(medication_notification_id, notif.day, notif.time, run_out_date.strftime('%Y-%m-%d %H:%M:%S'))

    return get_id[0][0]

for_user_cmd = """
    SELECT id, medication_id, rxcui, name, quantity, run_out_date, temporary, banned, possible_side_effects FROM user_meds
    WHERE user_id = %s
"""

get_med_cmd = """
    SELECT * from meds
    WHERE id = %s
"""

get_side_effects_command = """ SELECT possible_side_effects FROM meds WHERE rxcui = %s """

def get_drug_side_effects(rxcui):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(get_side_effects_command, [rxcui])
    side_effects_return = cursor.fetchall()

    try:
        return (((side_effects_return[0][0]).replace("\\", "")).replace(")", "")).replace("(", "")
    except:
        if not side_effects_return:
            return
        else:
            return side_effects_return

def for_user():
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)
    
    cursor.execute(for_user_cmd, [auth.uid()])
    users_meds = cursor.fetchall()

    for user_med in users_meds:
        med_id = user_med.get("medication_id")

        count = cursor.execute(get_med_cmd, [med_id])
        if count == 0:
            continue

        row = cursor.fetchone()

        del row["id"]
        user_med.update(row)


    return users_meds

def refill(med_id):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    cursor.execute("""
        SELECT * FROM user_meds
        WHERE id = %s
    """, [med_id])
    med = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM notifications
        WHERE medication_id = %s
    """, [med_id])
    notifs_db = cursor.fetchall()

    notifs = []
    for notif_db in notifs_db:
        day = notif_db["day_to_take"]
        time = notif_db["time_to_take"]

        notifs.append(Notification(day=day, time=time))

    run_out_date = calc_run_out_date(med.get("quantity"), notifs, start=dt.datetime.now())

    cursor.execute("""
        UPDATE user_meds
        SET run_out_date = %s
        WHERE id = %s
    """, [run_out_date, med_id])

    cursor.execute("""
        UPDATE notifications
        SET run_out_date = %s
        WHERE medication_id = %s
    """, [run_out_date, med_id])

    conn.commit()

    return run_out_date

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

get_user_leagues = """ SELECT league FROM users WHERE id = %s """

def check_leagues(cui, name):
    conn = db.conn()
    cursor = conn.cursor()
    leagues = cursor.execute(get_user_leagues, [auth.uid()])
    leagues = cursor.fetchall()

    if leagues[0][0] == "":
        return ""
    else:
        banned_cmd = """SELECT league FROM banned WHERE name like  %s"""
        cursor.execute(banned_cmd, [name.split(' ',1)[0]])
        return cursor.fetchall()


get_detailed_med_cmd = """ SELECT * FROM marigold.user_meds WHERE id = %s """

def get_detailed_med(id):
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(get_detailed_med_cmd, [id])
    info = cursor.fetchall()

    return info



        




