"""contains all the forms used on the webapp"""

from flask_wtf import Form
from wtforms.fields.html5 import DateField


class DatePickerForm(Form):
    """A simple form for picking the date"""
    start_date = DateField("Start Date", format='%Y-%m-%m')
    end_date = DateField("End Date", format='%Y-%m-%m')
