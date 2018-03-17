import time, datetime
import MySQLdb as sql
from MySQLdb.cursors import DictCursor


get_name = """ SELECT * FROM marigold.users WHERE id = %s """

def get_user_name(id):
	cursor.execute(get_name, [id])
	user = cursor.fetchall()

	for u in user :
		output = u[1] + " " + u[2]
		return output



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
	email = row[2]
	medication_id = row[3]
	name = row[4]
	day = row[5]
	time_to_take = row[6]
	user_name = get_user_name(user_id)

	now_time = datetime.datetime.now()
	upper_bound_time = datetime.datetime.now () + datetime.timedelta(minutes = 3)
	lower_bound_time = datetime.datetime.now () - datetime.timedelta(minutes = 3)


	time_print = "Now: " + str(now_time) + "|Lower " + str(lower_bound_time ) + "|Upper " + str(upper_bound_time)


	

	if(day == datetime.datetime.today().weekday() and time_to_take.time() > lower_bound_time.time() and time_to_take.time() < upper_bound_time.time()):
		output = "Hello "  + user_name + ". It is time to take " + name 
		print(output)
		#print(time_to_take.time())












