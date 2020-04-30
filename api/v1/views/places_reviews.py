#!/usr/bin/python3
""" place review """
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviewsPlace(place_id):
    """ reviews place
    """
    data = storage.get(Place, place_id)

    if not data:
        abort(404)

    if request.method == 'GET':
        info = [review.to_dict() for review in data.reviews]
        return jsonify(info)

    if request.method == 'POST':
        inf = request.get_json()
        if not inf:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in inf:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if not storage.get(User, inf['user_id']):
            abort(404)
        if 'text' not in inf:
            return make_response(jsonify({'error': 'Missing text'}), 400)

        inf['place_id'] = place_id
        review = Review(**inf)
        review.save()
        storage.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(review_id):
    """ reviews
    """
    data = storage.get(Review, review_id)

    if not data:
        abort(404)

    if request.method == 'GET':
        return jsonify(data.to_dict())

    if request.method == 'DELETE':
        data.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        info = request.get_json()

        if not info:
            abort(400, "Not a JSON")
        for i, value in info.items():
            if i not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                setattr(data, i, value)
        data.save()
        storage.save()
        return jsonify(data.to_dict()), 200
