"""The entry point for the application"""

from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta

from coronataiou.models import db, ma, RecordData, RecordSchema, IdRecordSchema
from coronataiou.forms import AddRecord, DatePickerForm

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        name = request.form['name']
        temperature = request.form['temperature']
        fatigue = request.form['fatigue']
        sore_throat = request.form['sore_throat']
        other_pain = request.form['other_pain']

        record_data = RecordData(name, temperature, fatigue, sore_throat, other_pain)

        db.session.add(record_data)
        db.session.commit()

        message = f"The data for {name} has been submitted"

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

    if request.method == "POST":
        change_form = AddRecord()
        if change_form.validate_on_submit():
            rec = RecordData.query.get(request.form['id_field'])
            rec.name = request.form['name']
            rec.temperature = request.form['temperature']
            rec.fatigue = request.form['fatigue']
            rec.sore_throat = request.form['sore_throat']
            rec.other_pain = request.form['other_pain']

            db.session.commit()

            message = f"The data for {request.form['name']} has been submitted"

            return render_template('add_record_temperature.html', message=message)
        else:
            for field, errors in change_form.errors.items():
                for error in errors:
                    flash("Error in {}: {}".format(
                        getattr(change_form, field).label.text,
                        error
                    ), 'error')
            return render_template('add_record_temperature.html', form1=change_form)

    # The start point for when an ID is selected
    if "edit" in request.args:
        id_search = int(request.args["edit"])
        query_res = RecordData.query.filter(RecordData.id == id_search).first()
        data = id_record_schema.dump(query_res)
        print(data)
        change_form = AddRecord(old_data=data)

        return render_template('add_record_temperature.html', form1=change_form)

    # redirect to delete if delete button clicked
    if "delete" in request.args:
        return redirect(url_for('delete', db_id=request.args['delete']), code=307)

    # The start point for when dates are selected
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

            # reformat date
            for datum in data:
                datum["updated"] = datum["updated"][:10]

            cols = ('id', 'name', 'temperature', 'sore_throat', 'fatigue', 'other_pain', 'updated')
            names = ('id', 'Name', 'Body Temperature', 'Sore Throat Pain?', 'Feeling Fatigue?', 'Other Pain?', 'Submission Date')
            table_header = dict(zip(cols, names))

            return render_template('edit.html', form=form, data=data, cols=cols, th=table_header, ds=default_start, de=default_end)

    return render_template('edit.html', form=form, data=data, cols=cols)


@app.route('/delete/<int:db_id>', methods=['GET', 'POST'])
def delete(db_id):
    if request.method == "POST":
        if "cancel" in request.form:
            return redirect(url_for("edit_table"), code=303)

        if "delete" in request.form:
            # TODO: データベースから削除　コード
            message = "The data has been deleted."
            return render_template('delete.html', message=message)

    cols = ('id', 'name', 'temperature', 'sore_throat', 'fatigue', 'other_pain', 'updated')
    names = ('id', 'Name', 'Body Temperature', 'Sore Throat Pain?', 'Feeling Fatigue?', 'Other Pain?', 'Submission Date')
    table_header = dict(zip(cols, names))

    data = RecordData.query.get(db_id)
    data = id_record_schema.dump(data)
    return render_template('delete.html', data=data, cols=cols, th=table_header)


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
    query_res = RecordData.query.filter(RecordData.updated >= convert_start).filter(RecordData.updated <= convert_end).order_by(RecordData.updated.desc()).all()

    return query_res


if __name__ == '__main__':
    app.run()
