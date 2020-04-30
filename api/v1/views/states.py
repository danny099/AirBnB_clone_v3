#!/usr/bin/python3
""" Show, Delete, Create and Update states """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def allStates(state_id=None):
    """ retrieves all states
        or retrieves one state by id
        state_id: id of the state to retrieve
    """
    allStates = storage.all('State')
    if not state_id:
        info = []
        for state in allStates.values():
            info.append(state.to_dict())
        return jsonify(info)
    else:
        state = "State.{}".format(state_id)
        if state in allStates:
            state = allStates[state]
            return jsonify(state.to_dict()), 200
        else:
            abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleteState(state_id):
    """ Deletes a specific state
        with the id
        state_id: id of the state to delete
    """
    allStates = storage.all('State')
    state = "State.{}".format(state_id)
    if state in allStates:
        state = allStates[state]
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def addState():
    """ creates a state
        with the information given
    """
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    if 'name' not in info:
        abort(400, 'Missing name')
    state = State(**info)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def editState(state_id):
    """ modifies a specific
    state with the id
    """
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    allStates = storage.all('State')
    state_id = "State.{}".format(state_id)
    if state_id in allStates:
        state = allStates[state_id]
        for key, value in info.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
