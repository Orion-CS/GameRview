from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class GameSearchForm(FlaskForm):
    searchText = StringField("searchText", validators=[InputRequired(), Length(0, 30)])
    submit = SubmitField("search")