#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def places_rewiew(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review)
    place_reviews = [v.to_dict() for k, v in reviews.items()
                     if getattr(v, 'place_id') == place_id]
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def reviews(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_del(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviews_post(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_dict = request.get_json(silent=True)
    if review_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'text' not in place_dict:
            return (jsonify({'error': 'Missing text'}), 400)
        if 'user_id' not in place_dict:
            return (jsonify({'error': 'Missing user_id'}), 400)
        else:
            user = storage.get(User, place_dict.get('user_id'))
            if user is None:
                abort(404)
        review_dict['place_id'] = place_id
        new_review = Review(**review_dict)
        new_review.save()
        return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviews_put(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_dict = request.get_json(silent=True)
    if review_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        for k, v in review_dict.items():
            if k not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                setattr(review, k, v)
            review.save()
            return (jsonify(review.to_dict()), 200)
