#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_get(state_id=None):
    """Returns states in storage"""
    if state_id is None:
        if request.method == 'GET':
            states_dict = [v.to_dict() for k, v in storage.all(State).items()]
            return jsonify(states_dict)
        elif request.method == 'POST':
            state_dict = request.get_json(silent=True)
            if state_dict is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            else:
                if 'name' not in state_dict:
                    return make_response(jsonify({'error': 'Missing name'}), 400)
                new_state = State(**state_dict)
                new_state.save()
                return make_response(jsonify(new_state.to_dict()), 201)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if request.method == 'GET':
            return (jsonify(state.to_dict()))
        if request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return (jsonify({}), 200)
        if request.method == 'PUT':
            state_dict = request.get_json(state_dict)
            if state_dict is None:
                abort(404)
            else:
                if (state_dict.get('name', None)) is None:
                    abort(404)
                for k, v in state_dict.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(state, k, v)
                    state.save()
                return (jsonify(state.to_dict()), 200)