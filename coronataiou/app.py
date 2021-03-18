"""The entry point for the application"""

from datetime import datetime, timedelta
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask import request, jsonify

from coronataiou.form import AddRecord
from coronataiou.models import db, ma, RecordData, RecordSchema


app = Flask(__name__)
app.config["DEBUG"] = True

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthdata.db'
db.init_app(app)
ma.init_app(app)

records_schema = RecordSchema(many=True)

with app.app_context():
    """Initializes the database"""
    db.create_all()

Bootstrap(app)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_record', methods=['GET','POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        name = request.form['name']
        temperature = request.form['temperature']
        fatigue = request.form['fatigue']
        sore_throat = request.form['sore_throat']
        other_pain = request.form['other_pain']

        print("hello")

        record_datas = RecordData(name, temperature, fatigue, sore_throat, other_pain)
        print(record_datas)

        db.session.add(record_datas)
        db.session.commit()

        message = f"THe data for {name} has been submitted"

        return render_template('add_record_temperature.html', message=message)
    else:
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record_temperature.html', form1=form1)

# select a record to edit or delete
# @app.route('/select_record/<letters>')
# def select_record(letters):
#     # alphabetical lists by name, chunked by letters between _ and _
#     # .between() evaluates first letter of a string
#     a, b = list(letters)
#     record_datas = record_data.query.filter(record_data.name.between(a, b)).order_by(record_data.name).all()
#     return render_template('select_record_temperature.html', record_data=record_datas)
#
# # edit or delete - come here from form in /select_record
# @app.route('/edit_or_delete', methods=['POST'])
# def edit_or_delete():
#     id = request.form['id']
#     choice = request.form['choice']
#     record_datas = record_data.query.filter(record_data.id == id).first()
#     # two forms in this template
#     form1 = AddRecord()
#     form2 = DeleteForm()
#     return render_template('edit_or_delete_temperature.html', record_data=record_datas, form1=form1, form2=form2, choice=choice)
#
#
# @app.route('/delete_result', methods=['POST'])
# def delete_result():
#     id = request.form['id_field']
#     purpose = request.form['purpose']
#     record_datas = record_data.query.filter(record_data.id == id).first()
#     if purpose == 'delete':
#         db.session.delete(record_datas)
#         db.session.commit()
#         message = f"The data {record_datas.name} has been deleted from the database."
#         return render_template('result.html', message=message)
#     else:
#         # this calls an error handler
#         abort(405)

# result of edit - this function updates the record
# @app.route('/edit_result', methods=['POST'])
# def edit_result():
#     id = request.form['id_field']
#     # call up the record from the database
#     record_datas = record_data.query.filter(record_data.id == id).first()
#     # update all values
#     record_datas.name = request.form['name']
#     record_datas.temperature = request.form['temperature']
#     record_datas.fatigue = request.form['fatigue']
#     record_datas.sore_throat = request.form['sore_throat']
#     record_datas.other_pain = request.form['other_pain']
#     # get today's date from function, above all the routes
#     record_datas.updated = stringdate()
#
#     form1 = AddRecord()
#     if form1.validate_on_submit():
#         # update database record
#         db.session.commit()
#         # create a message to send to the template
#         message = f"The data for {record_datas.name} has been updated."
#         return render_template('result.html', message=message)
#     else:
#         # show validaton errors
#         record_datas.id = id
#         # see https://pythonprogramming.net/flash-flask-tutorial/
#         for field, errors in form1.errors.items():
#             for error in errors:
#                 flash("Error in {}: {}".format(
#                     getattr(form1, field).label.text,
#                     error
#                 ), 'error')
#         return render_template('edit_or_delete.html', form1=form1, record_data=record_datas, choice='edit')
# +++++++++++++++++++++++



@app.route('/api/v1/name', methods=['GET'])
def api_name():
    if 'name' not in request.args:
        return "Please provide a name."


@app.route('/api/user/<string:name>', methods=['GET'])
def get_name(name):
    """Returns all records matching the name"""

    query_res = RecordData.query.filter_by(name=name).all()
    return jsonify(records_schema.dump(query_res))


@app.route('/api/date/<string:year>/<string:month>/<string:day>', methods=['GET'])
def get_date(year, month, day):
    """Returns all records for the selected date. Adjusts for Japan Timezone UTC+9"""

    try:
        converted_date = datetime.strptime("".join([year, month, day]), "%Y%m%d")
    except (ValueError, TypeError):
        return "Error: Use format of yyyy/mm/dd."
    name = request.args['name']
    query_str = "SELECT * FROM data WHERE name=?"
    res = dbutils.query_db(query_str, [name])
    if res:
        return jsonify(res)
    else:
        return "user not found"

    # timezone adjustment
    converted_date = converted_date - timedelta(hours=9)

    next_day = converted_date + timedelta(days=1)

    query_res = RecordData.query.filter(RecordData.updated >= converted_date).filter(RecordData.updated < next_day).all()
    return jsonify(records_schema.dump(query_res))


if __name__ == '__main__':
    app.run()
