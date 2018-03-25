import db
from error import Error

import requests as req
import collections as col


search_cmd = """SELECT id FROM marigold.meds WHERE rxcui = %s """

def get_rx(num):


	conn = db.conn()
	cursor = conn.cursor()
	cursor.execute(search_cmd, [num])
	number = cursor.fetchall()


	if not number:
		search = "https://api.fda.gov/drug/label.json?search=rxcui:" + num
		response = req.get(search)
		data = response.json()
		results = data.get('results')

		if results == None:
			return -1
		else:
			return insert_drug(num,results)
	else:
		return number[0][0]




def insert_drug(num,results):
		results = results[0]
		output = {}
		insert_cols = "rxcui, "
		insert_vals = "\"" +num + "\","

		if results.get('purpose') != None:
			purpose = ((results.get('purpose'))[0]).replace("\"", "")
			output['purpose'] = purpose[8:]

		if results.get('inactive_ingredient') != None:
			inactive_ingredient = (results.get('inactive_ingredient'))[0]
			output['inactive_ingredient'] = inactive_ingredient[21:]

		if results.get('warnings') != None:
			warnings = (results.get('warnings'))[0]
			output['warnings'] = warnings[9:]

		if results.get('questions') != None:
			output['questions'] = (results.get('questions'))[0]

		if results.get('when_using') != None:
			output['when_using'] = (results.get('when_using'))[0]

		if results.get('warnings_and_cautions') != None:
			output['warnings_and_cautions'] = ((results.get('warnings_and_cautions'))[0]).replace("\"","")

		if results.get('indications_and_usage') != None:
			output['indications_and_usage'] = (results.get('indications_and_usage'))[0]

		if results.get('openfda') != None:
			openfda = results.get('openfda')

			if openfda.get('generic_name') != None:
				output['generic_name'] = (openfda.get('generic_name'))[0]

			if openfda.get('brand_name') != None:
				output['brand_name'] = (openfda.get('brand_name'))[0]

		for x in output:
			insert_cols += x + ","
			insert_vals += "\"" + output[x] + "\" , "


		insert_cols = insert_cols[:-1]
		insert_vals = insert_vals[:-2]

		add_cmd = """ INSERT INTO marigold.meds (""" + insert_cols + """) VALUES (""" + insert_vals + """);"""

		conn = db.conn()
		cursor = conn.cursor()
		cursor.execute(add_cmd)

		cursor.execute(search_cmd, [num])
		number = cursor.fetchall()

		return number[0][0]

