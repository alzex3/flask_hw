from models import Advert

from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AdvertSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Advert

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
