"""The entry point for the application"""

import flask
from flask import request, jsonify, g

import db_utils

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/name', methods=['GET'])
def api_name():
    if 'name' not in request.args:
        return "Please provide a name."

    name = request.args['name']
    query_str = "SELECT * FROM data WHERE name=?"
    res = db_utils.query_db(query_str, [name])
    if res:
        return jsonify(res)
    else:
        return "user not found"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
