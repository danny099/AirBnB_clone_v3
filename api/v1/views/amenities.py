#!/usr/bin/python3
""" Show, Delete, Create and Update amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """ retrieves all amenities
        or retrieves one amenity by id

        amenity_id: id of the amenity to retrieve
    """
    data = storage.all('Amenity')
    if not amenity_id:
        info = []
        for amenity in data.values():
            info.append(amenity.to_dict())
        return jsonify(info)
    else:
        amenity = "Amenity.{}".format(amenity_id)
        if amenity in data:
            amenity = data[amenity]
            return jsonify(amenity.to_dict())
        else:
            abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes a specific amenity
        with the id

        amenity_id : id of the amenity to delete
    """
    data = storage.all('Amenity')
    amenity = "Amenity.{}".format(amenity_id)
    if amenity in data:
        amenity = data[amenity]
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """ creates a amenity
        with the information given
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(name=data['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_amenity(amenity_id):
    """modifies a specific
    amenity with the id
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    res = storage.all('Amenity')
    amenity_id = "Amenity.{}".format(amenity_id)
    if amenity_id in res:
        amenity = res[amenity_id]
        for key, value in data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        amenity.save()
        storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)