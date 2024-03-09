# Jack Manges, jm5244@drexel.edu
# Zane Hamdan, zih23@drexel.edu
# CS530: Final Project 

import os

from flask import Flask, g, json, render_template, request, session, redirect, jsonify, url_for
from passlib.hash import pbkdf2_sha256
from db import Database

DATABASE_PATH = 'spellcaster.db'

reference_classes = ["Choose...", "Bard", "Cleric", "Druid", "Fighter", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
reference_schools = ["Choose...", "Evocation", "Conjuration", "Abjuration", "Transmutation", "Enchantment", "Necromancy", "Divination", "Illusion"]
reference_levels = ["Choose...", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

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
    message = None
    message = request.args.get('message', None)
    if message is None:
            return render_template('home.html')
    else:
        return render_template('home.html', message=message)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/spell_reference', methods=['GET', 'POST'])
def spelllist():
    data = None
    spell_name, spell_class, spell_school, spell_level = None, None, None, None
    if request.method == 'POST':
        spell_name = request.form.get('form_name')
        spell_class, spell_school, spell_level = parse_reference_fields(request.form.get('form_class'), 
                                                                        request.form.get('form_school'), 
                                                                        request.form.get('form_level'))
        data = get_db().get_reference_spells(spell_name, spell_class, spell_school, spell_level)
    else:
        data = get_db().get_reference_spells("", "", "", "")

    return render_template('spell_reference.html', data=data, spell_name=spell_name, spell_class=spell_class, 
                           spell_school=spell_school, spell_level=spell_level, reference_classes=reference_classes, 
                           reference_levels=reference_levels, reference_schools=reference_schools)

def parse_reference_fields(spell_class, spell_school, spell_level):
    if spell_class == "Choose...":
        spell_class = ""
    if spell_school == "Choose...":
        spell_school = ""
    if spell_level == "Choose...":
        spell_level = ""
    return spell_class, spell_school, spell_level

@app.route('/spell_display', methods=['GET'])
def spell_display():
    data = None
    spell_name = request.args.get('data')
    data = get_db().get_spell(spell_name)
    return render_template('spell_display.html', spell_name=spell_name, data=data)

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
                confirm_message = "User creation successful!"
                return redirect(url_for('login', confirm_message=confirm_message))
            else:
                message = "Retyped password does not match typed password, please try again"
    return render_template('create_user.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    confirm_message = request.args.get('confirm_message', None)
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
    return render_template('login.html', message=message, confirm_message=confirm_message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/myloadouts', methods=['GET', 'POST'])
def myloadouts():
    if 'user' in session.keys():
        loadouts = get_db().get_user_loadouts(session['user']['id'])
        loadout_names = []
        unique_loadouts = []
        for loadout in loadouts:
            name = loadout[2]
            if name not in loadout_names:
                unique_loadouts.append(loadout)
                loadout_names.append(name)
        
        
        print(loadout_names)
        return render_template('myloadouts.html',loadouts = unique_loadouts)


@app.route('/loadout/<loadout_id>')
def loadout(loadout_id):
    spells = []
    if 'user' in session.keys():
        spells = get_db().get_loadout_spell_names(session['user']['id'], loadout_id)
        spells = [s[0] for s in spells]
        full_spells = []
        for spell in spells:
            full_spells.append(get_db().get_spell(spell))

        full_spells = [list(spell.values()) for spell in full_spells]

        n_spells = len(full_spells)

        return render_template('loadout.html', loadout_id=loadout_id, spells = full_spells,  n_spells =n_spells)


@app.route('/builder1')
def builder1():
    if 'user' in session.keys():
        return render_template('listbuilder1.html')
    message = "You must be logged in to build a loadout."
    return render_template('login.html', message=message)


@app.route('/builder2', methods=['GET', 'POST'])
def builder2():
    selected_class = request.form.get('class')
    desc = request.form.get('spellListDesc')
    spell_list_name = request.form.get('spellListName')
    print(request.form)
    #active_loadout = get_db().get_loadout_spell_names(session['user']['id'], spell_list_name)
    #active_loadout = [l[0] for l in active_loadout]
    #active_loadout_json = json.dumps(active_loadout)
    return render_template('listbuilder2.html', selected_class=selected_class, desc=desc, spell_list_name=spell_list_name)

@app.route('/api/class_spells', methods=['GET'])
def get_class_spell_list():
    selected_class = request.args.get('fetchedClass')
    return get_db().get_class_spells(selected_class)

@app.route('/api/delete_loadout', methods=['POST'])
def delete_loadout():
    loadout_name = request.form.get('loadout_name')
    if 'user' in session.keys():
        get_db().delete_loadout(session['user']['id'], loadout_name)

    return 'OKAY'

@app.route('/api/post_loadout', methods=['POST'])
def retrieve_loadout():
    print("Inside retrieve loadout function")
    loadout = request.form.getlist('loadout[]')
    loadout_name = request.form.get('spell_list_name')
    desc = request.form.get('list_desc')
    selected_class = request.form.get('selected_class')
    if 'user' in session.keys():
        get_db().delete_loadout(session['user']['id'], loadout_name)
        for spell in loadout:
            get_db().insert_spell_for_loadout(session['user']['id'], loadout_name, selected_class, desc, spell)
    
    return 'OKAY'

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
