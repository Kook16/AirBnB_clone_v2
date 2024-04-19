#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state_cities(id=None):
    """Displays a HTML page with a list of City objects linked to the State"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities_id(id):
    """Displays a HTML page with a list of City objects linked to the State"""
    states = storage.all(State).values()
    state = None
    for ids in states:
        if ids.id == id:
            state = ids
    return render_template("9-states.html", state=state, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
