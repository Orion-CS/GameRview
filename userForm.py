from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, Optional, Regexp, Email

class UserForm(FlaskForm):
    username = StringField("Username", validators=[Optional(), Length(6, 30), Regexp("^\w+$")])
    email = EmailField("Email", validators=[Optional(), Email()])
    submit = SubmitField("Update Credentials")    