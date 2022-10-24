#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_get(amenity_id=None):
    """Returns states in storage"""
    if amenity_id is None:
        if request.method == 'GET':
            amenities_dict = [v.to_dict() for k, v in storage.all(Amenity).items()]
            return jsonify(amenities_dict)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())



@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_del(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_post():
    amenity_dict = request.get_json(silent=True)
    if amenity_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in amenity_dict:
            return (jsonify({'error': 'Missing name'}), 400)
        new_amenity = Amenity(**amenity_dict)
        new_amenity.save()
        return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_dict = request.get_json(silent=True)
    if amenity_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        for k, v in amenity_dict.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
            amenity.save()
            return (jsonify(amenity.to_dict()), 200)
