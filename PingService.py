import requests
from flask_httpauth import HTTPDigestAuth
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import time
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret key 1 2 3'
auth = HTTPDigestAuth()
db = SQLAlchemy(app)

users = {"vcu": "rams"}


class ValidationError(ValueError):
    pass


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.errorhandler(404)
def error404(e):
    return '<h1> The page you are looking for does not exist.</h1>'


@app.errorhandler(500)
def error500(e):
    return '<h1> That did not work.</h1>'


@app.route('/ping', methods = ['GET'])
@auth.login_required
def ping():
    ping_time = time.time_ns() * 1000
    r = requests.get('https://smithpong.herokuapp.com/pong', auth=HTTPDigestAuth('vcu', 'rams'))
    pong_time = time.time_ns() * 1000
    elapsed = {
        "pingpong_t": pong_time - ping_time
    }
    return jsonify(elapsed, 201)


