# Jack Manges, jm5244@drexel.edu
# CS530: Assignment 1

import os

from flask import Flask, g, json, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/spelllist')
def spelllist():
    return render_template('bikes.html')

# From old template
#@app.route('/about2')
#def about2():
#    data = {
#        'related': [
#            {'name': 'Rent A Goat', 'url': 'http://rentagoat.com'},
#            {'name': 'We Rent Goats', 'url': 'http://werentgoats.com'},
#            {'name': 'Goat Yoga', 'url': 'https://goatyoga.net/'}
#        ]
#    }
#    return render_template('about2.html', data=data)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
