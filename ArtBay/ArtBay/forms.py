from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField, FileField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
from ArtBay.queries import get_user_by_user_name, get_user_by_pk
from ArtBay.utils.choices import ArtMediumChoices


class UserLoginForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user is None:
            raise ValidationError(f'User name "{self.user_name.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')


class UserSignupForm(FlaskForm):
    full_name = StringField('Full name',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Full name'))
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                                    validators=[DataRequired()],
                                    render_kw=dict(placeholder='Password'))
    submit = SubmitField('Sign up')

    def validate_user_name(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user:
            raise ValidationError(f'User name "{self.user_name.data}" already in use.')

    def validate_password_repeat(self, field):
        if not self.password.data == self.password_repeat.data:
            raise ValidationError(f'Provided passwords do not match.')


class FilterArtForm(FlaskForm):
    medium = SelectField('Medium',
                           choices=ArtMediumChoices.choices())
    sold_by = StringField('Sold by')
    price = FloatField('Price (lower than or equal to)',
                       validators=[NumberRange(min=0, max=100)])

    submit = SubmitField('Filter')


class AddArtForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    medium = SelectField('Medium',
                           validators=[DataRequired()],
                           choices=ArtMediumChoices.choices())
    price = IntegerField('Price',
                         validators=[DataRequired(), NumberRange(min=0, max=1000000)])
    artist_pk = IntegerField('Artist',
                             validators=[DataRequired()],
                             render_kw=dict(disabled='disabled'))
    descrip = StringField('Description', validators=[DataRequired()])
    image = StringField('Image File (must be .jpg)', validators=[Length(min=2, max=2000)])
    submit = SubmitField('Add art')


class BuyArtForm(FlaskForm):
    submit = SubmitField('Yes, buy it')