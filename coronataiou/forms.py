"""contains all the forms used on the webapp"""

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField


class DatePickerForm(FlaskForm):
    """A simple form for picking the date"""
    startdate = DateField("Start Date", format='%m-%d-%Y')
    enddate = DateField("End Date", format='%m-%d-%Y')
    submit = SubmitField('Search')
