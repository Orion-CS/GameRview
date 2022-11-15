from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Optional

class ReviewForm(FlaskForm):
    rating = SelectField(validators=[InputRequired()], choices=[1, 2, 3, 4, 5])
    review = StringField(validators=[Optional()])
    submit = SubmitField("Post Review")
    