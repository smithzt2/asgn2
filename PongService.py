import random
from requests.auth import HTTPDigestAuth
from flask import Flask, jsonify
import SQLAlchemy
from flask import app
import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'data.sqlite')
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
    return '<h1> That doesn\'t work.</h1>'


@app.route('/pong', methods=['GET'])
@auth.login_required
def pong():
    payload = {
        'rand': random.randint()
    }
    print(payload)
    return jsonify(payload, 201)


if __name__ == '__main__':
