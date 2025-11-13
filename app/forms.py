"""
Alliance Management System - Form Classes
Define forms with validations using Flask-WTF
"""

from flask_wtf import FlaskForm  
from wtforms import StringField, SelectField, SubmitField  
from wtforms.validators import DataRequired, Email, Length 


# Basic member form with validations
class MemberForm(FlaskForm):
    """Form for adding a new member with validations"""

    # Name field - required, must be 2-50 characters
    name = StringField(
        'Name',  
        validators=[
            DataRequired(message='Name is required'),  
            Length(min=2, max=50, message='Name must be between 2 and 50 characters')  
        ]
    )

    # Email field - required, must be valid email format
    email = StringField(
        'Email',  
        validators=[
            DataRequired(message='Email is required'),  
            Email(message='Must be a valid email address')  
        ]
    )

    # Role field - dropdown selection, required
    role = SelectField(
        'Role',  
        choices=[],  # Empty initially, can be set dynamically in route
        validators=[
            DataRequired(message='Role is required') 
        ]
    )

    # Submit button
    submit = SubmitField('Add Member')  # Button text


# Extended form - demonstrates subclassing (adding fields)
class ExtendedMemberForm(MemberForm):
    """Extended form that adds phone field to MemberForm"""

  
    phone = StringField(
        'Phone',  
        validators=[
            Length(max=15, message='Phone number cannot exceed 15 characters')  
        ]
    )
