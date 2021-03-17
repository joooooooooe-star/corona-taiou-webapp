"""The entry point for the application"""

from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta

from coronataiou.models import db, ma, RecordData, RecordSchema
from coronataiou.forms import DatePickerForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'muh_secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

records_schema = RecordSchema(many=True)

with app.app_context():
    """Initializes the database"""
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pickdate', methods=['GET', 'POST'])
def pick_date():
    """leads to a form where the date can be selected"""
    form = DatePickerForm()
    if form.validate_on_submit():
        # TODO: Get data and search database
        pass

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


if __name__ == '__main__':
    app.run()
