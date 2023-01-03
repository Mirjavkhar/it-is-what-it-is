from wtforms import Form, StringField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import PasswordInput

# ===== Forms  ===== #

class LoginForm(Form):
    email = EmailField('Email', validators=[InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired("Please enter the password.")])
    remember = BooleanField('Remember me')

class SignUpForm(Form):
    username = StringField('Name', validators=[Length(min=3, max=20), InputRequired()])
    email = EmailField('Email', validators=[InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired("Please enter the password.")])
    password_confirm = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired("Please enter the password.")])
