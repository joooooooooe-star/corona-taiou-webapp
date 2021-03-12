"""The entry point for the application"""

from flask import Flask, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from datetime import date
from flask import request, jsonify, g

from coronataiou import dbutils

app = Flask(__name__)
app.config["DEBUG"] = True

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

# Flask-Bootstrap requires this line
Bootstrap(app)
# the name of the database; add path if necessary
db_name = 'Daily_temperature_checkup.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class record_data(db.Model):
    __tablename__ = 'daily_record'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    temperature = db.Column(db.Float)
    fatigue = db.Column(db.String)
    sore_throat = db.Column(db.String)
    other_pain = db.Column(db.String)
    updated = db.Column(db.String)

    def __init__(self, name, temperature, fatigue, sore_throat, other_pain,updated):
        self.name = name
        self.temperature = temperature
        self.fatigue = fatigue
        self.sore_throat = sore_throat
        self.other_pain = other_pain
        self.updated = updated


# +++++++++++++++++++++++
# forms with Flask-WTF

# form for add_record and edit_or_delete
# each field includes validation requirements and messages

class AddRecord(FlaskForm):
    id_field = HiddenField()
    name = StringField('Name', [InputRequired(),
                                Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid name"),
                                Length(min=3, max=25, message="Invalid name")
                                ])
    temperature = FloatField('temperature ℃', [InputRequired(),
                                               NumberRange(min=1.00, max=99.99, message="Invalid range")
                                               ])
    fatigue = SelectField('Do you feel fatigue ', [InputRequired()],
                          choices=[('', ''), ('Yes', 'Yes'),('No','No') ])

    sore_throat = SelectField('Does your feel sore hurt? ', [InputRequired()],
                              choices=[('', ''), ('Yes', 'Yes'),('No','No') ])
    other_pain = SelectField('Do you have any other pain? ', [InputRequired()],
                             choices=[('', ''), ('Yes', 'Yes'),('No','No') ])

    update = HiddenField()
    submit = SubmitField('Add/Update Record')


class DeleteForm(FlaskForm):
    id_filed = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Delete this data')


def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    # build string in format 01-01-2000
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return date_string

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

        updated = stringdate()
        record_datas = record_data(name,temperature,fatigue,sore_throat,other_pain,updated)

        db.session.add(record_datas)
        db.session.commit()

        message = f"THe data for {name} has been submitted"

        return render_template('add_record_temperature.html', message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record_temperature.html', form1=form1)

# select a record to edit or delete
@app.route('/select_record/<letters>')
def select_record(letters):
    # alphabetical lists by sock name, chunked by letters between _ and _
    # .between() evaluates first letter of a string
    a, b = list(letters)
    record_datas = record_data.query.filter(record_data.name.between(a, b)).order_by(record_data.name).all()
    return render_template('select_record_temperature.html', record_data=record_datas)

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    record_datas = record_data.query.filter(record_data.id == id).first()
    # two forms in this template
    form1 = AddRecord()
    form2 = DeleteForm()
    return render_template('edit_or_delete_temperature.html', record_data=record_datas, form1=form1, form2=form2, choice=choice)


@app.route('/delete_result', methods=['POST'])
def delete_result():
    id = request.form['id_field']
    purpose = request.form['purpose']
    record_datas = record_data.query.filter(record_data.id == id).first()
    if purpose == 'delete':
        db.session.delete(record_datas)
        db.session.commit()
        message = f"The data {record_datas.name} has been deleted from the database."
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)

# result of edit - this function updates the record
@app.route('/edit_result', methods=['POST'])
def edit_result():
    id = request.form['id_field']
    # call up the record from the database
    record_datas = record_data.query.filter(record_data.id == id).first()
    # update all values
    record_data.name = request.form['name']
    record_data.temperature = request.form['temperature']
    record_data.fatigue = request.form['fatigue']
    record_data.sore_throat = request.form['sore_throat']
    record_data.other_pain = request.form['other_pain']
    # get today's date from function, above all the routes
    record_data.updated = stringdate()

    form1 = AddRecord()
    if form1.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"The data for sock {record_data.name} has been updated."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        record_data.id = id
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, record_datas=record_data, choice='edit')

@app.route('/api/v1/name', methods=['GET'])
def api_name():
    if 'name' not in request.args:
        return "Please provide a name."

    name = request.args['name']
    query_str = "SELECT * FROM data WHERE name=?"
    res = dbutils.query_db(query_str, [name])
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
