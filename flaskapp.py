from flask import Flask, render_template, request
import subprocess

import users.routes

app = Flask(__name__)

app.register_blueprint(users.routes.blueprint, url_prefix='/users')

@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
	return render_template('hello.html', name=name)




@app.route('/update/git', methods = ['GET', 'POST'])
def update():
	cmd = ["./hook.sh", ]
	return "hi"

if __name__ == '__main__':
  app.run(debug=True)
