#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State


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
        else:
            user = storage.get(User, place_dict.get('user_id'))
            if user is None:
                print("I do get here")
                abort(404)
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

@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search places on fields provided in body """
    # get the request body
    body_dict = request.get_json(silent=True)
    result = []
    city_ids = []
    # if its not valid json raise 400 error with m = Not a JSON
    if body_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # get all place objects and city objects
    places = storage.all(Place)
    cities = storage.all(City)
    # if json body is empty, or each list of all keys are empty, return all place objects
    if not body_dict.get('States') and not body_dict.get('Cities') \
            and not body_dict.get('Amenities'):
        result = [v.to_dict() for k, v in places.items()]
        return (jsonify(result), 200)
    # if states not empty-> get all city for each state, return all places for each of those cities;
    if body_dict.get('States'):
        state_ids = body_dict.get('States')
        city_ids = [v.id for k, v in cities.items() if city.state_id in state_ids]
    # if cities not empty-> if city not in above state, return all places for each of those cities;
    if body_dict.get('Cities'):
        city_ids += body_dict.get('Cities')
        city_ids = list(set(city_ids))

    all_places = [v for k, v in places.items() if v.city_id in city_ids]
    # if amenities not empty -> filter result in the above for places that have all amenities attached
    if body_dict.get('Amenities'):
        amenities = [storage.get(Amenity, a_id) for a_id in body_dict.get('Amenities')]
        result = [v.to_dict() for v in all_places if all(am in v.amenities for am in amenities)]
    else:
        result = [v.to_dict() for v in all_places]
    # return the result
    return (jsonify(result), 200)
