from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, widgets, MultipleFileField, IntegerField, DecimalField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from my_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken! Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken! Please choose a different one.')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    buy_or_rent = RadioField('Type of Sale', validators=[DataRequired()], choices=[('Buy', 'Buy'), ('Rent', 'Rent')])
    content = TextAreaField('Description', validators=[DataRequired()])
    amenities = MultiCheckboxField('Amenities', validators=[DataRequired(message='Please choose at least one of the options above.')], choices=[('A/C', 'A/C'), ('Fully Equipped Kitchen', 'Fully equipped kitchen'), ('WI-FI', 'WIFI'), ('Washing Machine', 'Washing Machine'), ('Dryer', 'Dryer'), ('None', 'None')])
    master_bedroom = FileField('Master Bedroom', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    master_bathroom = FileField('Master Bathroom', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    kitchen = FileField('Kitchen', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    outside_view = FileField('Outside View', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    house_pictures = MultipleFileField('House photos (multiple files allowed)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    address_line_1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line_2 = StringField('Address Line 2')
    city = SelectField(u'City', choices=['Adjuntas', 'Aguada', 'Aguadilla', 'Aguas Buenas', 'Aibonito', 'Añasco', 'Arecibo', 'Arroyo', 'Barceloneta', 'Barranquitas', 'Bayamón',
                                         'Cabo Rojo', 'Caguas', 'Camuy', 'Canóvanas', 'Carolina', 'Cataño', 'Cayey', 'Ceiba', 'Ciales', 'Cidra', 'Coamo', 'Comerío',
                                         'Corozal', 'Culebra', 'Dorado', 'Fajardo', 'Florida', 'Guánica', 'Guayama', 'Guayanilla', 'Guaynabo', 'Gurabo', 'Hatillo', 'Hormigueros',
                                         'Humacao', 'Isabela', 'Jayuya', 'Juana Díaz', 'Juncos', 'Lajas', 'Lares', 'Las Marías', 'Las Piedras', 'Loíza', 'Luquillo',
                                         'Manatí', 'Maricao', 'Maunabo', 'Mayagüez', 'Moca', 'Morovis', 'Naguabo', 'Naranjito', 'Orocovis', 'Patillas', 'Peñuelas',
                                         'Ponce', 'Quebradillas', 'Rincón', 'Río Grande', 'Sabana Grande', 'Salinas', 'San Germán', 'San Juan', 'San Lorenzo',
                                         'San Sebastián', 'Santa Isabel', 'Toa Alta', 'Toa Baja', 'Trujillo Alto', 'Utuado', 'Vega Alta', 'Vega Baja', 'Vieques',
                                         'Villalba', 'Yabucoa', 'Yauco'], validators=[DataRequired()])
    state_province_region = StringField('State / Province / Region', validators=[DataRequired()])
    zip_postal_code = StringField('ZIP / Postal Code', validators=[DataRequired()])
    number_of_bedrooms = IntegerField('Number of Bedrooms', validators=[DataRequired()])
    number_of_bathrooms = IntegerField('Number of Bathrooms', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    submit = SubmitField('Post')
