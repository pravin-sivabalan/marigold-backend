import time, datetime
import MySQLdb as sql
from MySQLdb.cursors import DictCursor


get_name = """ SELECT * FROM marigold.users WHERE id = %s """

def get_user_name(id):
	cursor.execute(get_name, [id])
	user = cursor.fetchall()

	for u in user :
		return u[1], u[2], u[3]

get_med = """ SELECT * FROM marigold.user_meds WHERE id = %s """

def get_med_name(med_id):
	cursor.execute(get_med, [med_id])
	med = cursor.fetchall()

	for m in med:
		return m[3]


def make_conn():
	conn = sql.connect (host = "marigold.czubge8ebda6.us-east-1.rds.amazonaws.com",
                        user = "marigold",
                        passwd = "PQ2M4A2fdZ0wz7",
                        db = "marigold")
	return conn


conn = make_conn()
cursor = conn.cursor()

select_notification = """
    SELECT * FROM notifications;
"""

cursor.execute(select_notification)
conn.commit()

data = cursor.fetchall()

for row in data :
	id = row[0]
	user_id = row[1]
	
	medication_id = row[2]
	med_name = get_med_name(medication_id)

	day = row[3]
	time_to_take = row[4]
	
	first_name, last_name, email = get_user_name(user_id)
	user_name = first_name + " " + last_name



	now_time = datetime.datetime.now() 
	upper_bound_time = datetime.datetime.now () + datetime.timedelta(minutes = 3) 
	lower_bound_time = datetime.datetime.now () - datetime.timedelta(minutes = 3)


	if(day == datetime.datetime.today().weekday() and time_to_take.time() > lower_bound_time.time() and time_to_take.time() < upper_bound_time.time()):
		output = "Hello "  + user_name + ". It is time to take " + str(med_name)
		print(output)
	else:
		if(time_to_take):
			time_print = "Lower: " + str(lower_bound_time.time()) + " Time_to_take: " + str(time_to_take.time())
			print(time_print)












