from flask import request, jsonify, Blueprint, json, render_template, flash, redirect, url_for

import auth
import base64, string, random
from base64 import decodestring
from PIL import Image
from error import Error, MissingDataError
from io import BytesIO
from time import sleep
import os

import re, locale
import meds.db
import meds.lookup
import meds.conflict
import meds.fda
import meds.by_symptom
import meds.allergy
import users.db

import requests as req
import collections as col

blueprint = Blueprint("web", __name__)

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/register')
def register():
    return render_template('register-form.html')

@blueprint.route('/login', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		return render_template('login-form.html', error="Incorrect Credentials")
	else:
		return render_template('login-form.html', error="")

@blueprint.route('/login/submit', methods=['POST', 'GET'])
def login_submit():
	email, password = "", ""

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
	elif request.method == 'GET':
		username = request.args.get('email')
		password = request.args.get('password')

		if username != " " and password != " ":
			return render_template('index.html')

	try:
		users.db.check_creds(email, password)
		return render_template('index.html')
	except:
		return redirect(url_for('web.login'), code=307)


@blueprint.route('/register/submit', methods=['POST', 'GET'])
def register_submit():
	if request.method == 'POST':
		email = request.form['email']
		first = request.form['first']
		last = request.form['last']
		password = request.form['password']
		allergies = request.form['allergies']
		paddress = request.form['paddress']
		pname = request.form['pname']
		pphone = request.form['pphone']
		NBA = "NBA" in request.form
		NFL = "NFL" in request.form
		NCAA = "NCAA" in request.form
	else:
		email = request.args.get('email')
		password = request.args.get('password')
		cpassword = request.args.get('cpassword')

		if password == cpassword:
			return render_template('index.html')
		else:
			return redirect(url_for('web.login'), code=307)
    
