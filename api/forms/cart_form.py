from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class AddToCartForm(FlaskForm):
    quantity = SelectField(
        'Quantity',
        validators=[DataRequired()],
        choices=[('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')]
    )
    submit = SubmitField('Add to Cart')