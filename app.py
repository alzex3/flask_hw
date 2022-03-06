from flask import Flask, jsonify, request
from flask.views import MethodView

from models import db, Advert
from schemes import ma, AdvertSchema
from validators import is_valid, is_exist

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)


advert_schema = AdvertSchema()
adverts_schema = AdvertSchema(many=True)


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


app.add_url_rule('/api/adverts', view_func=AdvertsAPI.as_view('adverts'), methods=['POST', 'GET'])
app.add_url_rule('/api/advert/<int:advert_id>', view_func=AdvertAPI.as_view('advert'), methods=['GET', 'DELETE'])
