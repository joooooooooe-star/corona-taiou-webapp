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

    # timezone adjustment
    converted_date = converted_date - timedelta(hours=9)

    next_day = converted_date + timedelta(days=1)

    query_res = RecordData.query.filter(RecordData.updated >= converted_date).filter(
        RecordData.updated < next_day).all()
    return jsonify(records_schema.dump(query_res))


if __name__ == '__main__':
    app.run()
