from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Optional

class UserSearchForm(FlaskForm):
    searchText = StringField("searchText", validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField("search")