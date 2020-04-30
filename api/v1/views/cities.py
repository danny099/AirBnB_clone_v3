#!/usr/bin/python3
""" states """
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_state(state_id):
    """
        get y post
    """
    data = storage.get(State, state_id)

    if not data:
        abort(404)

    info = []
    for info in data.cities:
        info.append(info.to_dict())
    if request.method == 'GET':
        return jsonify(info)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        args = request.get_json()
        args['state_id'] = state_id
        city = City(**args)
        city.save()
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def citiesId(city_id):
    """
        cities id
    """
    data = storage.get(City, city_id)

    if not data:
        abort(404)

    if request.method == 'GET':
        return jsonify(data.to_dict())

    if request.method == 'DELETE':
        data.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(data, attr, val)
        data.save()
        return jsonify(data.to_dict())