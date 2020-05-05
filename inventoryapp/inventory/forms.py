from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class InventoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    size = StringField('Size')
    count = DecimalField('Count', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add item')


class UpdateInventoryItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    size = StringField('Size')
    count = DecimalField('Count', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Update item')
