from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired()])
    # validate password
    password = PasswordField("Password: ", validators=[InputRequired()])
    submit = SubmitField("Submit: ")
    