
import time, datetime

import db
import auth

from error import Error

add_cmd = """ INSERT INTO marigold.notifications (user_id, medication_id, day_to_take, time_to_take, run_out_date) VALUES (%s, %s, %s, %s, %s); """
get_id_of_add = """SELECT id FROM marigold.notifications WHERE user_id = %s AND medication_id = %s AND day_to_take = %s AND time_to_take = %s """

def add(medication_id, day_to_take, time_to_take, run_out_date):
	conn = db.conn()
	cursor =  conn.cursor()

	#print(add_cmd % (auth.uid(), medication_id, day_to_take, time_to_take, run_out_date))

	cursor.execute(add_cmd, [auth.uid(), medication_id, day_to_take, time_to_take, run_out_date] )

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

cal_cmd = """SELECT * FROM marigold.notifications WHERE user_id = %s"""

def is_next_days(today, check):

	if check == today:
		return 1

	lower = today - 5
	upper = today + 5


	if lower < 0:
		lower = 0
	else:
		lower = today - minus_number


	if upper > 6:
		upper = 6


	print(lower, check, upper)


	if check <= lower:
		return 1

	if check >= upper:
		return 1




def cal(user_id):
	conn = db.conn()
	cursor =  conn.cursor()
	cursor.execute(cal_cmd, [user_id])
	res = cursor.fetchall()


	output = []

	for x in res:
		row = {}
		row['medication_id'] = x[2]
		row['day_to_take'] = x[3]
		row['time_to_take'] = x[4]
		row['run_out_date'] = x[5]

		now_time = datetime.datetime.now() 
		number = datetime.datetime.today().weekday()

		#print(number, x[3])

		if x[5] > now_time:
			output.append(row)
		
		

	return output
