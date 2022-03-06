from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.Date, default=datetime.now())
    owner = db.Column(db.String(30), nullable=False)
