# -*- coding: utf-8 -*-
"""Form objects

This module contains form objects, extensions of the Flask Form, used for
user input principally the 'Add Alarm Form'.
"""
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired
from wtforms.validators import Required
from wtforms.validators import ValidationError

class AddAlarmForm(FlaskForm):
    """An extension of Flask WTF Forms for adding an alarm. Attributes
    represent fields.

    Attributes:
        name (StringField): New alarm's name field.
        time (DateTimeLocalField): New alarm's time to go off at.
        add (SubmitField): Button to submit form.

    Methods:
        A validation function to ensure the time entered isn't in the past.
    """
    name = StringField("Name", validators=[DataRequired()])
    time = DateTimeLocalField("Time",
                              format='%Y-%m-%dT%H:%M',
                              validators=[Required()])
    # Format for time field: Year-month-day-hour-minutes
    # This format is later adjusted for a different display format.

    add = SubmitField("Add")

    def validate_time(self, field: DateTimeLocalField) -> datetime:
        """This function which runs when the form submits checks the time
        field and ensures that if the time has passed, the form does not submit
        and raises a ValidationError
        
        Args:
            field (DateTimeLocalField): time field.
        
        Returns:
            Field data if validated.
        
        Raises:
            ValidationError: If the time is in the past.
        """
        if field.data <= datetime.now():
            raise ValidationError("The time cannot be in the past!")
        return field.data
