from flask import request, jsonify, Blueprint, json, render_template


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

import requests as req
import collections as col

blueprint = Blueprint("web", __name__)

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/login')
def login():
    return render_template('login-form.html')

@blueprint.route('/login/submit', methods=['POST'])
def login_submit():
    email = request.form['email']
    first = request.form['first']
    last = request.form['last']
    return email + "<br>" + first + " " + last
