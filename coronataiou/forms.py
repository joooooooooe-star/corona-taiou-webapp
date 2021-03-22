"""contains all the forms used on the webapp"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, HiddenField, StringField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange


class DatePickerForm(FlaskForm):
    """A simple form for picking the date"""
    startdate = DateField("Start Date", format='%m-%d-%Y')
    enddate = DateField("End Date", format='%m-%d-%Y')
    submit = SubmitField('Search')


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

    def __init__(self, old_data=None, *args, **kwargs):
        super(AddRecord, self).__init__(*args, **kwargs)
        if old_data:
            self.id_field.data = old_data["id"]
            self.name.data = old_data["name"]
            self.temperature.data = old_data["temperature"]
            self.fatigue.data = old_data["fatigue"]
            self.sore_throat.data = old_data["sore_throat"]
            self.other_pain.data = old_data["other_pain"]
