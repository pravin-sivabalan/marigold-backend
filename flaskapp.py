from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, session

import click

import subprocess
import os
import users.routes
import meds.routes
import update.routes
import notification.routes


import db
import db.util
import users.db


import boto3
from botocore.exceptions import ClientError

from error import Error, response_for_error

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.register_blueprint(users.routes.blueprint, url_prefix='/user')
app.register_blueprint(meds.routes.blueprint, url_prefix='/meds')
app.register_blueprint(update.routes.blueprint, url_prefix='/update')
app.register_blueprint(notification.routes.blueprint, url_prefix='/notification')


@app.errorhandler(Error)
def handle_error(error):
    return response_for_error(error)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon1.ico')

@app.route('/update/git', methods = ['GET', 'POST'])
def update():
	cmd = ["./hook.sh", ]
	return "hi"

@app.route('/database/connectiontest')
def connectiokn_test():
        config = db.config.read()
        output = "User: " + config['database']['user'] + "<br>Host: " + config['database']['host'] 
        
        return output

@app.route('/img/<img>')
def post_image(img):
    file_to_return = "static/img/" + img
    return send_file(file_to_return)




# Command Line Utils
# NOT ACCESSIBLE BY  DONT WORRY
# Use like so on terminal: `flask $CMD_NAME_HERE $ARG1 $ARG2 ... $ARGN

@app.cli.command("init-db")
def db_init(*args, **kwargs):
    db.util.init(*args, **kwargs)

@app.cli.command("add-user")
@click.option("--first", default="FIRST")
@click.option("--last", default="LAST")
@click.option("--email", default="EMAIL")
@click.option("--passwd", default="PASSWD")
def db_add_user(first, last, email, passwd):
    db.util.add_user(first, last, email, passwd)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        return render_template('register-form.html', error="User Already Exists")
    else:
        return render_template('register-form.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return render_template('login-form.html', error="Incorrect Credentials")
    else:
        return render_template('login-form.html', error="")

@app.route('/login/submit', methods=['POST', 'GET'])
def login_submit():
    email, password = "", ""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    elif request.method == 'GET':
        username = request.args.get('email')
        password = request.args.get('password')

    app.logger.error('An error occurred')
    try:
        out = users.db.check_creds(email, password)
        session['login'] = out
        return redirect(url_for('dashboard'))
    except:
        return redirect(url_for('login'), code=307)


@app.route('/register/submit', methods=['POST', 'GET'])
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

        league = ""
        if NBA == True:
            league += "NBA,"
        if NFL == True:
            league += "NFL,"
        if NCAA == True:
            league += "NCAA,"

        leagues = league[:-1]

        try:
            users.db.create_user(first, last, email, password, leagues, allergies, pname, pphone, paddress)
            session["login"] = users.db.find_user_email(email)
        except:
            return redirect(url_for('register'), code=307)

        return redirect(url_for('dashboard'))

    else:
        email = request.args.get('email')
        password = request.args.get('password')
        cpassword = request.args.get('cpassword')

        if password == cpassword:
            return render_template('index.html')
        else:
            return redirect(url_for('login'), code=307)


@app.route('/dashboard')
def dashboard():
    if 'login' in session:
        user_id = session['login']
        user_meds = users.db.get_meds(user_id)
        return render_template('dashboard.html', user_id=user_id, meds = user_meds)
    else:
        return redirect(url_for('index'))


@app.route('/detailed/<med_id>')
def detailed(med_id):
    if 'login' in session:
        user_id = session['login']
        return render_template('detailed.html', med_id=med_id, user_id=user_id, med_info=meds.db.get_detailed_med(med_id))
    else:
        return redirect(url_for('index'))

def listify(list_str):
    items = [item.strip() for item in list_str.split(",")]
    items = [item for item in items if item != ""]

    return items

@app.route('/account/<id>')
def account(id):
    if 'login' in session:
            user_id = session['login']
            user = users.db.find_user(user_id)

            return render_template('account_detailed.html', user_id=user_id, user=user, 
                allergies = listify(user["allergies"]),
                leagues = listify(user["league"]))
    else:
            return redirect(url_for('index'))

  

if __name__ == '__main__':
  app.run(debug=True)
