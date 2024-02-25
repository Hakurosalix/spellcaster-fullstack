import os
import sqlite3
from flask import Flask, g, json, render_template, request

app = Flask(__name__)

DATABASE = 'data/spells.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/builder1')
def builder1():
    return render_template('listbuilder1.html')



@app.route('/builder2', methods=['POST'])
def builder2():
    selected_class = (request.form['class'])
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM spell_info WHERE Classes LIKE '%{selected_class}%'")
    all_spells = cursor.fetchall()
    return render_template('listbuilder2.html', all_spells=all_spells)




if __name__ == "__main__":
    app.run(host='localhost',port=8080, debug=True)