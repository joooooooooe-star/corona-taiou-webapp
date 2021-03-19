"""Contains all the database models to be used"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()


class RecordData(db.Model):
    __tablename__ = 'daily_record'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    temperature = db.Column(db.Float)
    fatigue = db.Column(db.String(3))
    sore_throat = db.Column(db.String(3))
    other_pain = db.Column(db.String(3))
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, temperature, fatigue, sore_throat, other_pain, **kwargs):
        super(RecordData, self).__init__(**kwargs)
        self.name = name
        self.temperature = temperature
        self.fatigue = fatigue
        self.sore_throat = sore_throat
        self.other_pain = other_pain


class RecordSchema(ma.SQLAlchemySchema):
    class Meta:
        # Return everything but id and update time
        model = RecordData

    name = ma.auto_field()
    temperature = ma.auto_field()
    fatigue = ma.auto_field()
    sore_throat = ma.auto_field()
    other_pain = ma.auto_field()
    updated = ma.auto_field()
