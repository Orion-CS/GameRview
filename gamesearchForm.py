from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Optional

class GameSearchForm(FlaskForm):
    searchText = StringField("searchText", validators=[Length(min=0, max=30)])
    submit = SubmitField("search")