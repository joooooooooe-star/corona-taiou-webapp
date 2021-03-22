"""The entry point for the application"""

from flask import Flask, jsonify, render_template, request, flash, abort
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta

from coronataiou.form import AddRecord
from coronataiou.models import db, ma, RecordData, RecordSchema, IdRecordSchema
from coronataiou.forms import DatePickerForm

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthdata.db'
db.init_app(app)
ma.init_app(app)

records_schema = RecordSchema(many=True)
id_records_schema = IdRecordSchema(many=True)
id_record_schema = IdRecordSchema()

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


@app.route('/add_record', methods=['GET', 'POST'])
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


@app.route('/edit', methods=['GET', 'POST'])
def edit_table(data=None, cols=None):
    """The endpoint containing the feature to edit and remove data"""

    form = DatePickerForm()

    if all(["startdate" in request.args, "enddate" in request.args]):

        default_start = request.args["startdate"]
        default_end = request.args["enddate"]
        convert_start = datetime.strptime(default_start, "%Y-%m-%d")
        convert_end = datetime.strptime(default_end, "%Y-%m-%d")

        # Validate the dates
        if convert_start > convert_end:
            flash("Please make sure the start date is before the end date.")
            return render_template('edit.html', form=form, data=None, cols=None)

        # Pull data and flash message if no data found
        result = request.args
        db_res = get_week_data(result)
        if not db_res:
            flash("no data found")
        else:
            data = id_records_schema.dump(db_res)
            cols = ('id', 'name', 'temperature', 'sore_throat', 'fatigue', 'other_pain', 'updated')
            return render_template('edit.html', form=form, data=data, cols=cols, ds=default_start, de=default_end)

    return render_template('edit.html', form=form, data=data, cols=cols)


@app.route('/delete', methods=['GET'])
def delete():
    if 'remove' in request.args:
        cols = ('id', 'name', 'temperature', 'sore_throat', 'fatigue', 'other_pain', 'updated')
        data = RecordData.query.filter_by(id=int(request.args['lineIdEdit'])).first()
        data = id_record_schema.dump(data)
        return render_template('delete.html', data=data, col=cols)


@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_id(pk_id):
    pass

"""Start of the API Routes"""


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

    # timezone adjustment
    converted_date = converted_date - timedelta(hours=9)

    next_day = converted_date + timedelta(days=1)

    query_res = RecordData.query.filter(RecordData.updated >= converted_date).filter(
        RecordData.updated < next_day).all()
    return jsonify(records_schema.dump(query_res))


def get_week_data(result: dict) -> dict:
    convert_start = datetime.strptime(result["startdate"], "%Y-%m-%d") - timedelta(hours=9)
    convert_end = datetime.strptime(result["enddate"], "%Y-%m-%d") + timedelta(hours=13)
    query_res = RecordData.query.filter(RecordData.updated >= convert_start).filter(RecordData.updated <= convert_end).all()

    return query_res


if __name__ == '__main__':
    app.run()
