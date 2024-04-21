#!/usr/bin/python3
'''Starts a Flask web application
'''
from flask import Flask
import sys


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    '''Display Hello HBNB!'''
    return ('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Display HBNB!'''
    return ('HBNB!')


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    '''display “C ” followed by the value of the text variable
    '''
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    '''display “Python”, followed by the value of the text variable
    '''
    return "Python {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
