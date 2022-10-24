#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def users_get(user_id=None):
    """Returns states in storage"""
    if user_id is None:
        if request.method == 'GET':
            users_dict = [v.to_dict()
                          for k, v in
                          storage.all(User).items()]
            return jsonify(users_dict)
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def users_del(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def users_post():
    user_dict = request.get_json(silent=True)
    if user_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'email' not in user_dict:
            return (jsonify({'error': 'Missing email'}), 400)
        if 'password' not in user_dict:
            return (jsonify({'error': 'Missing password'}), 400)
        new_user = User(**user_dict)
        new_user.save()
        return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def users_put(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_dict = request.get_json(silent=True)
    if user_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        for k, v in user_dict.items():
            if k not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user, k, v)
            user.save()
            return (jsonify(user.to_dict()), 200)
