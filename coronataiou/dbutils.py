"""Contains functions to access and relinquish control of the database"""

import sqlite3
from flask import g
from flask import current_app as app

DATABASE = 'healthinfo.db'


def dict_factory(cursor, row):

    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    """returns the db object"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = dict_factory
    return db


def init_db() -> None:
    """if no db exists, creates one"""
    with app.app_context():
        db = get_db()
        with app.open_resource('../schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query: str, args=(), one=False):
    """Runs a specified query and returns results"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    print(rv[0])
    return (rv[0] if rv else None) if one else rv
