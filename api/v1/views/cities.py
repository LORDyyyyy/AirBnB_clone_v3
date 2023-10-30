#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_citis(state_id):
    """ get all cities by states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City).values()
    cities = [val for val in cities if val.state_id == state_id]
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get city using id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ add a new city in the database"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
