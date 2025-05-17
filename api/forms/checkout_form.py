from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class CheckoutForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField(
        'State', validators=[DataRequired()],
        choices=[('QLD', 'Queensland'), ('NSW', 'New South Wales'), ('VIC', 'Victoria'), ('SA', 'South Australia'), ('WA', 'Western Australia'), ('TAS', 'Tasmania'), ('ACT', 'Australian Capital Territory   ')],
        default='QLD',
        coerce=str
        )
    zip_code = IntegerField('ZIP Code', validators=[DataRequired()])
    submit = SubmitField('Place Order')