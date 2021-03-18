from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange


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