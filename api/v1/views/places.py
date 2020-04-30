#!/usr/bin/python3
""" show status """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_of_city(city_id):
    """
        Retrieves the list of all Place objects of a City
        city_id: Is the id of the searched city
    """
    data = storage.get(City, city_id)

    if not data:
        abort(404)

    info = []
    for info in data.places:
        info.append(info.to_dict())
    if request.method == 'GET':
        return jsonify(info)

    if request.method == 'POST':
        res = request.get_json()
        if not res:
            abort(400, 'Not a JSON')
        if "user_id" not in res:
            abort(400, 'Missing user_id')
        if storage.get(User, res["user_id"]) is None:
            abort(404)
        if "name" not in res:
            abort(400, 'Missing name')

        res['city_id'] = city_id
        newPlace = Place(**res)
        newPlace.save()
        storage.save()
        return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places_by_id(place_id):
    """
        Retrieves the list of all Place objects of a City
        place_id: is the id of the searched place
    """
    data = storage.get(Place, place_id)

    if not data:
        abort(404)

    if request.method == 'GET':
        return jsonify(data.to_dict())

    if request.method == 'DELETE':
        storage.delete(data)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        res = request.get_json()
        if not res:
            abort(400, "Not a JSON")
        dont = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
        for key, value in res.items():
            if key in dont:
                pass
            else:
                setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
