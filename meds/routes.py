
from flask import request, jsonify, Blueprint, json


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

import rx.relation as rxrel

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

@blueprint.route('/search', methods = ['POST'])
@auth.required
def search():
    data = request.get_json()
    try:
        symptom = data["symptom"]
    except KeyError as err:
        raise MissingDataError(err)

    class_id = rxrel.class_by_name(symptom, types=["DISEASE"])
    if class_id is None:
        return jsonify(message="none")

    drugs = meds.by_symptom.perform(class_id.cid)
    return jsonify(message="ok", drugs=drugs)

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
        refill = data["refill"]
    except KeyError as err:
        raise MissingDataError(err)

    med_id = meds.db.add(name, cui, quantity, notifications, temporary, alert_user)
    return jsonify(message="ok", 
        conflicts=meds.conflict.check_with_id(med_id), 
        allergy_conflicts=meds.allergy.check(med_id),
        banned_leagues=meds.db.check_leagues(cui, name))


@blueprint.route('/for-user', methods = ['GET'])
@auth.required
def for_user():
    users_meds = meds.db.for_user()
    return jsonify(message="ok", meds=users_meds)

@blueprint.route('/conflicts', methods = ['GET'])
@auth.required
def conflicts():
    return jsonify(message="ok", 
        conflicts=meds.conflict.check(),
        allergy_conflicts=meds.allergy.check_all())

@blueprint.route('/conflicts-with/<cui>', methods = ['GET'])
@auth.required
def conflicts_with(cui):
    return jsonify(message="ok",
        conflicts=meds.conflict.check_with(cui),
        allergy_conflicts=meds.allergy.check_with(cui))

@blueprint.route('/refill', methods = ['POST'])
@auth.required
def refill():
    data = request.get_json()

    try:
        med_id = data["med_id"]
    except KeyError as err:
        raise MissingDataError(err)

    meds.db.refill(med_id)
    return jsonify(message="ok")

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

    bad_words = open("/var/www/html/flaskapp/bad_words.txt", "r")
    bad_words_list = bad_words.read().split(',')

    data = request.get_json()
    picture_data = data["photo"]
    image_data = bytes(picture_data, encoding="ascii")
    file_name_o = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]) + ".png"
    file_name = "/home/ubuntu/flaskapp/static/img/" + file_name_o

    with open(file_name,"wb") as f:
        f.write(decodestring(image_data))


    try:
        search_url = "https://api.ocr.space/parse/image"
        headers = {"apikey":"8cec6b890688957","Content-Type":"application/json"}

        payload = {
            'language':'eng',
            'isOverlayRequired':'true',
            'apikey':'8cec6b890688957'
        }


        with open(file_name, "rb") as f: 
            r = req.post(
                'https://api.ocr.space/parse/image',
                files={file_name: f},
                data=payload
            )

        output = r.content.decode()
        output = json.loads(output)
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

        best_word = ""
        best_size = 0

        for w in good_words:
            try:
                matches = meds.lookup.perform(w)

                if len(matches) > best_size:
                    best_word = w
                sleep(0.1)
            except:
                pass

        if best_word == "":
            return jsonify(message="Could not read label successfully.")


        best_match = meds.lookup.perform(best_word)

    except:
        return jsonify(message="Could not read label successfully.")

    return jsonify(message="ok", matches=best_match)
