
import MySQLdb as sql
from MySQLdb.cursors import DictCursor

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

first_name = "Hello"
id = 6


cursor.execute(select_notification)
conn.commit()

data = cursor.fetchall()

for row in data :
	print (row[0], row[1], row[2], row[3], row[4], row[5])


print(make_conn())
print("Hello World")
