#!/usr/bin/python3
"""Model that creates the place_amenities api blueprint """
from flask import jsonify
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [v.to_dict() for v in place.amenities()]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenitiy(place_id, amenity_id):
    """ """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amentiy, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity not in place.amenities():
            abort(404)
        place.amenity_ids.remove(amenity.id)
    place.save()
    return (jsonify({}), 200)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amentiy, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()), 200)
        place.amenities.add(amenity)
    else:
        if amenity in place.amenities():
            return (jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity.id)
    place.save()
    return (jsonify(amenity.to_dict()), 201)
