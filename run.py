# Jack Manges, jm5244@drexel.edu
# CS530: Assignment 1

import os

from flask import Flask, g, json, render_template, request, session, redirect, jsonify
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


@app.route('/spell_reference', methods=['GET', 'POST'])
def spelllist():
    data = None
    if request.method == 'POST':
        spell_name = request.form.get('spell_name')
        spell_class = request.form.get('spell_class')
        spell_school = request.form.get('spell_school')
        spell_level = request.form.get('spell_level')
        if spell_class == "Choose...":
            spell_class = ""
        if spell_school == "Choose...":
            spell_school = ""
        if spell_level == "Choose...":
            spell_level = ""
        data = get_db().get_reference_spells(spell_name, spell_class, spell_school, spell_level)
    else:
        data = get_db().get_reference_spells("", "", "", "")
    
    return render_template('spell_reference.html', data=data)

    

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

@app.route('/builder1')
def builder1():
    if 'user' in session.keys():
        return render_template('listbuilder1.html')
    message = "You must be logged in to do that."
    return render_template('login.html', message=message)

@app.route('/builder2', methods=['POST'])
def builder2():
    selected_class = (request.form['class'])
    desc = request.form.get('spellListDesc')
    spell_list_name = request.form.get('spellListName')
    return render_template('listbuilder2.html', selected_class=selected_class, desc=desc, spell_list_name=spell_list_name)

@app.route('/api/class_spells', methods=['GET'])
def get_class_spell_list():
    selected_class = request.args.get('fetchedClass')
    return get_db().get_class_spells(selected_class)

@app.route('/api/post_loadout', methods=['POST'])
def retrieve_loadout():
    loadout = request.form.getlist('loadout[]')
    loadout_name = request.form.get('spell_list_name')
    desc = request.form.get('list_desc')
    selected_class = request.form.get('selected_class')
    if 'user' in session.keys():
        for spell in loadout:
            get_db().insert_spell_for_loadout(session['user']['id'], loadout_name, selected_class, desc, spell)
        loadout_table = (get_db().get_user_loadouts(session['user']['id']), "got loadout")

        
    
    return redirect('/')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
