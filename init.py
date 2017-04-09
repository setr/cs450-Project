from flask import Flask, request, render_template
from flask import url_for, redirect, session

import db
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/security')
def sec():
    data = db.getAllSecurity()
    return render_template('secview.html', data=data)

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    passw = request.form.get('password')
    if not user or not passw:
        raise BadInput('Missing Username or Password')

    data = db.login(user, passw)
    if not data:
        raise BadInput('Incorrect Username/Password')
    return render_template('index.html', data=data)
