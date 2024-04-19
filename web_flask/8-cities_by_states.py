#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """ Teardown method """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def display_cities_by_states():
    """ Displays a HTML page with a list of states and their cities """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=sorted_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
