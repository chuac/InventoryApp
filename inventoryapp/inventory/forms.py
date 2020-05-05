from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class InventoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    size = StringField('Size')
    count = DecimalField('Count', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add item')
