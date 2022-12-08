from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, Optional, Regexp, Email

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(6, 30), Regexp("^\w+$"), Optional()])
    email = EmailField("Email", validators=[InputRequired(), Email(), Optional()])
    submit = SubmitField("Update Credentials")    