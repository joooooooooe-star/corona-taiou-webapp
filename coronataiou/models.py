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

    def __init__(self, name, temperature, fatigue, sore_throat, other_pain, updated):
        self.name = name
        self.temperature = temperature
        self.fatigue = fatigue
        self.sore_throat = sore_throat
        self.other_pain = other_pain
        self.updated = updated


class ChangedRecordData(db.Model):
    """Contains the records for any data that has been modified."""
    __tablename__ = 'changed_records'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer)
    oldname = db.Column(db.String)
    newname = db.Column(db.String)
    oldtemperature = db.Column(db.Float)
    newtemperature = db.Column(db.Float)
    oldfatigue = db.Column(db.Boolean)
    newfatigue = db.Column(db.Boolean)
    oldsore_throat = db.Column(db.Boolean)
    newsore_throat = db.Column(db.Boolean)
    oldother_pain = db.Column(db.Boolean)
    newother_pain = db.Column(db.Boolean)
    dateofchange = db.Column(db.DateTime, default=datetime.utcnow)


class RemovedRecordData(db.Model):
    """Contains the records for any data that has been deleted."""
    __tablename__ = 'deleted_records'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer)
    name = db.Column(db.String)
    temperature = db.Column(db.Float)
    fatigue = db.Column(db.Boolean)
    sore_throat = db.Column(db.Boolean)
    oldother_pain = db.Column(db.Boolean)
    lastupdated = db.Column(db.DateTime)
    delete_date = db.Column(db.DateTime, default=datetime.utcnow)


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


class IdRecordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RecordData

    id = ma.auto_field()
    name = ma.auto_field()
    temperature = ma.auto_field()
    fatigue = ma.auto_field()
    sore_throat = ma.auto_field()
    other_pain = ma.auto_field()
    updated = ma.auto_field()

