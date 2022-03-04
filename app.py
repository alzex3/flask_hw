from datetime import datetime

from flask import Flask, jsonify, request, helpers
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


# Models ans schemes
class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.Date, default=datetime.now())
    owner = db.Column(db.String(30), nullable=False)


class AdvertSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Advert

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)


advert_schema = AdvertSchema()
adverts_schema = AdvertSchema(many=True)


# Validators
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


# Views
class AdvertsAPI(MethodView):
    @is_valid
    def post(self):
        rq = request.get_json()

        new_advert = Advert(
            title=rq['title'],
            description=rq['description'],
            owner=rq['owner'],
        )

        db.session.add(new_advert)
        db.session.commit()

        return advert_schema.jsonify(new_advert)

    # noinspection PyMethodMayBeStatic
    def get(self):
        adverts = Advert.query.all()

        return adverts_schema.jsonify(adverts)


class AdvertAPI(MethodView):
    @is_exist
    def get(self, advert_id):
        advert = Advert.query.get(advert_id)

        return advert_schema.jsonify(advert)

    @is_exist
    def delete(self, advert_id):
        advert = Advert.query.get(advert_id)

        db.session.delete(advert)
        db.session.commit()

        return jsonify()


# Router
app.add_url_rule('/api/adverts', view_func=AdvertsAPI.as_view('adverts'), methods=['POST', 'GET'])
app.add_url_rule('/api/advert/<int:advert_id>', view_func=AdvertAPI.as_view('advert'), methods=['GET', 'DELETE'])
