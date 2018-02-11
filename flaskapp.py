from flask import Flask, render_template, request

import subprocess

import users.routes

import db.util
import db.config

app = Flask(__name__)
app.register_blueprint(users.routes.blueprint, url_prefix='/user')

@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
	return render_template('hello.html', name=name)

@app.route('/update/git', methods = ['GET', 'POST'])
def update():
	cmd = ["./hook.sh", ]
	return "hi"

@app.route('/database/connectiontest')
def connectiokn_test():
        config = db.config.read()
        output = "User: " + config['database']['user'] + "<br>Host: " + config['database']['host'] 
        
        return output

@app.cli.command("init-db")
def db_init():
    db.util.init()

if __name__ == '__main__':
  app.run(debug=True)
