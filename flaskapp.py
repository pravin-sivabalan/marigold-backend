from flask import Flask, render_template, request
import click

import subprocess

import users.routes

import db
import db.util

from error import Error, response_for_error

app = Flask(__name__)
app.register_blueprint(users.routes.blueprint, url_prefix='/user')

@app.errorhandler(Error)
def handle_error(error):
    return response_for_error(error)

# Command Line Utils
# NOT ACCESSIBLE BY WEB, DONT WORRY
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

if __name__ == '__main__':
  app.run(debug=True)
