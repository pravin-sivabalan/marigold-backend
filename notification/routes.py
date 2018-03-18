from flask import request, jsonify, Blueprint, render_template, request

import auth
import auth.token

import notification.db
from error import Error, MissingDataError

blueprint = Blueprint('notification', __name__)


@blueprint.route('/add', methods = ['POST'])
@auth.required
def add():
	data = request.get_json()

	try:
		medication_id = data["medication_id"]
		day_to_take = data["day_to_take"]
		time_to_take = data["time_to_take"]
	except KeyError as err:
		raise MissingDataError(err)

	notification_id = notification.db.add(medication_id, day_to_take, time_to_take)


	return jsonify(message="ok", notification_id = notification_id)




@blueprint.route('/remove', methods = ['POST'])
@auth.required
def remove():
	data = request.get_json()

	try:
		medication_id = data["medication_id"]
	except KeyError as err:
		raise MissingDataError(err)

	out = notification.db.remove(medication_id)

	if out == 1:
		return jsonify(message="ok")
	else:
		return jsonify(error="1", message="Notification not found")
