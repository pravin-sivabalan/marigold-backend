from flask import request, jsonify, Blueprint, render_template, request

import auth
import auth.token

import users.db
import users.email as em

import boto3
from botocore.exceptions import ClientError

blueprint = Blueprint('users', __name__)

@blueprint.route('', methods = ['GET'])
@auth.required
def profile():
    return jsonify(
        message="ok",
        profile=users.db.user_profile(auth.uid())
    )

@blueprint.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    user = data.get('email')
    passwd = data.get('password')

    user_id = users.db.check_creds(user, passwd)

    return jsonify(
        message="ok",
        jwt=auth.token.create(user_id).decode("utf-8")
    )

@blueprint.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    league = data.get('league')
    allergies = data.get('allergies')
    pname = data.get('pharmacy_name')
    pnumber = data.get('pharmacy_number')
    paddress = data.get('pharmacy_address')

    user_id = users.db.create_user(first_name, last_name, email, password, league, allergies, pname, pnumber, paddress)
    return jsonify(
        message="ok",
        jwt=auth.token.create(user_id).decode("utf-8")
    )

@blueprint.route('/delete', methods = ['POST'])
@auth.required
def delete():
    users.db.delete_user(auth.uid())
    return jsonify(message="ok")


@blueprint.route('/change-password/<email>')
def change_password_user(email):
    return em.change_password(email)

@blueprint.route('/update-password/<link>')
def pdate_password_user(link):
    return render_template('password.html', link=link)


@blueprint.route('/user_change_password', methods = ['POST'])
def user_change_password():

    if request.method == 'POST':
      link = request.form['link']
      password = auth.calc_hash(request.form['password'])
      em.update_password(link, password)
      return "Thank you for reseting your password"


@blueprint.route('/delete-user/<email>')
def delete_user(email):
    return em.delete_account_email(email)
