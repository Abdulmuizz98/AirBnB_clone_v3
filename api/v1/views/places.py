#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def cities_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    city_places = [v.to_dict() for k, v in places.items()
                    if getattr(v, 'city_id') == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_del(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_dict = request.get_json(silent=True)
    if place_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in place_dict:
            return (jsonify({'error': 'Missing name'}), 400)
        if 'user_id' not in place_dict:
            return (jsonify({'error': 'Missing user_id'}), 400)
        place_dict['city_id'] = city_id
        new_place = Place(**place_dict)
        new_place.save()
        return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_dict = request.get_json(silent=True)
    if place_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        for k, v in place_dict.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(place, k, v)
            place.save()
            return (jsonify(place.to_dict()), 200)
