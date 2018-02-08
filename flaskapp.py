from flask import Flask, render_template, request
import configparser 

import subprocess
import users.routes

app = Flask(__name__)
app.register_blueprint(users.routes.blueprint, url_prefix='/user')


#Databse ini parse
parser = configparser.ConfigParser()
parser.sections()
parser.read('../database.ini')


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
        
        output = "User: " + parser['database']['user'] + "<br>Host: " + parser['database']['host'] 
        return output









if __name__ == '__main__':
  app.run(debug=True)
