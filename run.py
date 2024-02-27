# Jack Manges, jm5244@drexel.edu
# CS530: Assignment 1

import os

from flask import Flask, g, json, render_template, request, session, redirect
from passlib.hash import pbkdf2_sha256
from db import Database

DATABASE_PATH = 'spellcaster.db'

app = Flask(__name__)
app.secret_key = b'demokeynotreal!'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(DATABASE_PATH)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/spelllist')
def spelllist():
    return render_template('bikes.html')

@app.route('/class_builder', methods=['GET'])
def class_builder():
    if 'user' in session.keys():
        return render_template('class_builder.html')
    message = "You must be logged in to do that."
    return render_template('login.html', message=message)
    

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        retyped_password = request.form.get('retyped_password')
        if username and typed_password and retyped_password:
            if typed_password == retyped_password:
                encrypted_password = pbkdf2_sha256.hash(typed_password)
                get_db().create_user(username, encrypted_password)
                return redirect('/login')
            else:
                message = "Retyped password does not match typed password, please try again"
    return render_template('create_user.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
