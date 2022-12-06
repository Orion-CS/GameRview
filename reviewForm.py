from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional

class ReviewForm(FlaskForm):
    rating = SelectField(validators=[InputRequired()], choices=[1, 2, 3, 4, 5])
    review = TextAreaField("Rview", validators=[Optional(), Length(0, 1024)])
    submit = SubmitField("Post Rview")
    