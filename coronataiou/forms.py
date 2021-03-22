from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class InputForm(FlaskForm):
    name = StringField('Enter your name')
    temperature = StringField('Enter your temperature')
    condition = SelectField('Do you have malaise ?', choices=[('Yes'), ( 'No')])
    condition1 = SelectField('Do you have sore throat ?', choices=[('Yes'), ( 'No')])
    condition2 = SelectField('Do you have other illness ?', choices=[('Yes'), ('No')])
    submit = SubmitField('Submit')
