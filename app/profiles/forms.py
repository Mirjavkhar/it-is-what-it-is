from wtforms import Form, StringField, TextAreaField, FileField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email
from wtforms.widgets import PasswordInput

# ===== Forms  ===== #

class ProfileEditForm(Form):
    # name = StringField('Name')
    # email = EmailField('Email', validators=[Email("This field requires a valid email address")])
    about = TextAreaField('content')
    avatar = FileField('file')
    del_ava = BooleanField('del_ava')
    # password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired("Please enter the password.")])

class ChangePassForm(Form):
    password_initial = StringField('password', widget=PasswordInput(hide_value=True), validators=[InputRequired("Please enter the password.")])
    password = StringField('password', widget=PasswordInput(hide_value=True), validators=[InputRequired("Please enter the password.")])
    password_confirm = StringField('password_confirm', widget=PasswordInput(hide_value=True), validators=[InputRequired("Please confirm the password.")])

class ChangeEmailForm(Form):
    email = EmailField('email', validators=[Email()])    
    email_confirm = EmailField('email_confirm', validators=[Email()])    
    password = StringField('password', widget=PasswordInput(hide_value=False))