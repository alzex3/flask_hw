from flask import jsonify, request, helpers
from marshmallow import ValidationError

from models import Advert
from schemes import AdvertSchema


def is_valid(func):
    def wrapper(*args, **kwargs):
        try:
            AdvertSchema().load(request.get_json())

        except ValidationError as err:
            resp = helpers.make_response(jsonify(error=err.messages), 400)
            return resp

        result = func(*args, **kwargs)
        return result

    wrapper.__name__ = func.__name__
    return wrapper


def is_exist(func):
    def wrapper(*args, **kwargs):
        try:
            advert_id = request.view_args.get('advert_id')
            if not Advert.query.get(advert_id):
                raise AssertionError

        except AssertionError:
            resp = helpers.make_response(jsonify(error='Advert not found!'), 404)
            return resp

        result = func(*args, **kwargs)
        return result

    wrapper.__name__ = func.__name__
    return wrapper
