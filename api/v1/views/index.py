#!/usr/bin/python3
"""index API"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def show_count():
    """show_count"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    data = {}

    for key, cls in classes.items():
        data[key.lower()] = storage.count(cls)

    return jsonify(data)
