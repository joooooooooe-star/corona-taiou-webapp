"""The entry point for the application"""

from flask import Flask, jsonify, render_template, request, flash, abort
from datetime import datetime, timedelta

from coronataiou.models import db, ma, RecordData, RecordSchema, IdRecordSchema
from coronataiou.forms import DatePickerForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'muh_secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

records_schema = RecordSchema(many=True)
id_records_schema = IdRecordSchema(many=True)
id_record_schema = IdRecordSchema()

with app.app_context():
    """Initializes the database"""
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/edittable/', methods=['GET', 'POST'])
def edit_table():

    if request.method == "POST":
        return "not yet implemented"

    if 'edit' in request.args:
        # TODO: Link to input form with fields filled out
        id_data = RecordData.query.filter(RecordData.id == request.args['lineIdEdit'])
        return f"not yet implemented for edit"

    if 'remove' in request.args:
        cols = ('id', 'name', 'temperature', 'sore_throat', 'fatigue', 'other_pain', 'updated')
        data = RecordData.query.filter_by(id=int(request.args['lineIdEdit'])).first()
        data = id_record_schema.dump(data)
        return render_template('delete.html', data=data, col=cols)

    else:
        form = DatePickerForm()
        if form.is_submitted():
            # TODO: Add validators
            result = request.form
            db_res = get_week_data(result)
            if not db_res:
                flash("no data found")
            else:
                data = id_records_schema.dump(db_res)
                cols = ('id', 'name', 'temperature', 'sore_throat', 'fatigue', 'other_pain', 'updated')
                flash("found ur data")
                return render_template('edittable.html', data=data, cols=cols)

        return render_template('date.html', form=form)


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

    query_res = RecordData.query.filter(RecordData.updated >= converted_date).filter(RecordData.updated < next_day).all()
    return jsonify(records_schema.dump(query_res))


def get_week_data(result: dict) -> dict:
    convert_start = datetime.strptime(result["startdate"], "%Y-%m-%d") - timedelta(hours=9)
    convert_end = datetime.strptime(result["enddate"], "%Y-%m-%d") + timedelta(hours=13)
    query_res = RecordData.query.filter(RecordData.updated >= convert_start).filter(RecordData.updated <= convert_end).all()

    return query_res


if __name__ == '__main__':
    app.run()
