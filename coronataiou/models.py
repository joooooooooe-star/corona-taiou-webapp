"""Contains all the database models to be used"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class RecordData(db.Model):
    __tablename__ = 'daily_record'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    temperature = db.Column(db.Float)
    fatigue = db.Column(db.Boolean)
    sore_throat = db.Column(db.Boolean)
    other_pain = db.Column(db.Boolean)
    updated = db.Column(db.DateTime)

    def __init__(self, name, temperature, fatigue, sore_throat, other_pain, updated):
        self.name = name
        self.temperature = temperature
        self.fatigue = fatigue
        self.sore_throat = sore_throat
        self.other_pain = other_pain
        self.updated = updated


class RecordSchema(ma.Schema):
    class Meta:
        # Return everything but id and update time
        fields = ("name", "temperature", "fatigue", "sore_throat", "other_pain")
