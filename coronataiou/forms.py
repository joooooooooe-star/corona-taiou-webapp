"""contains all the forms used on the webapp"""

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from wtforms import SubmitField


class DatePickerForm(Form):
    """A simple form for picking the date"""
    startdate = DateField("Start Date", format='%Y-%m-%m')
    enddate = DateField("End Date", format='%Y-%m-%m')
    submit = SubmitField('Search')

