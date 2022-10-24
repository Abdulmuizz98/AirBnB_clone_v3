#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def states_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    state_cities = [v.to_dict() for k, v in cities.items()
                    if getattr(v, 'state_id') == state_id]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_del(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_post(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_dict = request.get_json(silent=True)
    if city_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in city_dict:
            return (jsonify({'error': 'Missing name'}), 400)
        city_dict['state_id'] = state_id
        new_city = City(**city_dict)
        new_city.save()
        return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_dict = request.get_json(silent=True)
    if city_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        for k, v in city_dict.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
            city.save()
            return (jsonify(city.to_dict()), 200)
