from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    # email, password, submit attribute
    email = StringField('Email', validators = [DataRequired(), Email()]) # the data required and email are used to validate the user input
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField() 
