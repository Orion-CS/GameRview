from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(6, 30), Regexp("^\w+$")])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=64)])
    # fix confirm password not working
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", 'Passwords must match')])
    submit = SubmitField("Create Account")