#!/usr/bin/python3
'''Starts a Flask web application
'''
from flask import Flask, render_template
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
def c_text(text):
    '''display “C ” followed by the value of the text variable
    '''
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    '''display “Python”, followed by the value of the text variable
    '''
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    '''display “n is a number” only if n is an integer
    '''
    return (f'{n} is a number')


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    '''display “n is a number” only if n is an integer
    '''
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_even_or_odd(n):
    '''isplay a HTML page only if n is an integer:
        H1 tag: “Number: n is even|odd” inside the tag BODY
    '''
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
