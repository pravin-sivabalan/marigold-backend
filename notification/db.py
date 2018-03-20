
import datetime as dt

import db
import auth

from error import Error

add_cmd = """ INSERT INTO marigold.notifications (user_id, medication_id, day_to_take, time_to_take) VALUES (%s, %s, %s, %s); """
get_id_of_add = """SELECT id FROM marigold.notifications WHERE user_id = %s AND medication_id = %s AND day_to_take = %s AND time_to_take = %s """

def add(medication_id, day_to_take, time_to_take):
	conn = db.conn()
	cursor =  conn.cursor()

	cursor.execute(add_cmd, [auth.uid(), medication_id, day_to_take, time_to_take])

	cursor.execute(get_id_of_add, [auth.uid(), medication_id, day_to_take, time_to_take])
	notification_id = cursor.fetchall()[0]
	conn.commit()
	return notification_id



remove_cmd = """ DELETE FROM marigold.notifications WHERE id = %s """

def remove(medication_id):
	conn = db.conn()
	cursor =  conn.cursor()

	count = cursor.execute(remove_cmd, [medication_id])
	
	if count == 0:
		return 0
	else:
		return 1

		
	conn.commit()

