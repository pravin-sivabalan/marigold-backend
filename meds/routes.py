
from flask import request, jsonify, Blueprint, json

import auth
import base64, string, random
from PIL import Image
from error import Error, MissingDataError
from io import BytesIO

import re, locale
import meds.db
import meds.lookup
import meds.conflict
import meds.fda

import requests as req
import collections as col

blueprint = Blueprint("meds", __name__)

@blueprint.route('/lookup', methods = ['POST'])
@auth.required
def lookup():
    data = request.get_json()
        
    try:
        name = data["name"]
    except KeyError as err:
        raise MissingDataError(err)

    matches = meds.lookup.perform(name)
    return jsonify(message="ok", matches=matches)

@blueprint.route('/add', methods = ['POST'])
@auth.required
def add():
    data = request.get_json()
        
    try:
        cui = data["cui"]
        name = data["name"]
        quantity = data["quantity"]
        notifications = data["notifications"]
        temporary = data["temporary"]
        alert_user = data["alert_user"]
    except KeyError as err:
        raise MissingDataError(err)


    meds.db.add(name, cui, quantity, notifications, temporary, alert_user)
    return jsonify(message="ok", conflicts=meds.conflict.check())

@blueprint.route('/for-user', methods = ['GET'])
@auth.required
def for_user():
    users_meds = meds.db.for_user()
    return jsonify(message="ok", meds=users_meds)

@blueprint.route('/conflicts', methods = ['GET'])
@auth.required
def conflicts():
    conflicts = meds.conflict.check()
    return jsonify(message="ok", conflicts=conflicts)

@blueprint.route('/delete', methods = ['POST'])
@auth.required
def delete():
    data = request.get_json()

    try:
        med_id = data["id"]
    except KeyError as err:
        raise MissingDataError(err)

    meds.db.delete(med_id)
    return jsonify(message="ok")



@blueprint.route('/pic', methods = ['POST'])
@auth.required
def picture():

    bad_words = open("bad_words.txt", "r")
    bad_words_list = bad_words.read().split(',')

    data = request.get_json()
    picture_data = data["photo"]
    image_data = bytes(picture_data, encoding="ascii")


    file_name_o = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]) + ".png"
    file_name = "static/img/" + file_name_o
    pic_url = "https://marigoldapp.net/img/" + file_name_o

    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im.save(file_name)


    try:
        search_url = "https://api.ocr.space/parse/image"
        headers = {"apikey":"8cec6b890688957","Content-Type":"application/json"}

        payload = {
            'language':'eng',
            'isOverlayRequired':'true',
            'url': pic_url,
            'apikey':'8cec6b890688957'
        }

        response = req.post(search_url, data=payload)
        output = response.json()


        results = output.get('ParsedResults')
        text = results[0]
        lines = text.get('TextOverlay').get('Lines')
        words_list = []


        for e in lines:
            line = e.get('Words')
            for l in line:
                word = l.get('WordText')
                if re.sub(r'[^a-zA-Z ]', '', word) and len(re.sub(r'[^a-zA-Z ]', '', word)) > 3:
                    words_list.append((re.sub(r'[^a-zA-Z ]', '', word)).lower())

        good_words = [x for x in words_list if x not in bad_words_list]

        print(good_words)
        print()


    except:
        return jsonify(message="Could not read label successfully.")

    
    print("Hello World")

    return jsonify(message="ok")
