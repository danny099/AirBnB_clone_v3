#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import *

@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def getAll(state_id=None):
    """ Endpoint that retrieves all states
        or retrieves one state by id

            state_id: id of the state to retrieve
    """
    allStates = storage.all('State')
    if not state_id:
        stateInfo = []
        for state in allStates.values():
            stateInfo.append(state.to_dict())
        return jsonify(stateInfo)
    else:
        state = "State.{}".format(state_id)
        if state in allStates:
            state = allStates[state]
            return jsonify(state.to_dict()), 200
        else:
            abort(404)
