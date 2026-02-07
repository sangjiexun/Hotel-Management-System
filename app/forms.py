from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    fullname = StringField('Full Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    teamId = SelectField('Team', coerce=int, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class RoomForm(FlaskForm):
    roomName = StringField('Room Name', validators=[DataRequired()])
    telephone = BooleanField('Telephone')
    projector = BooleanField('Projector')
    whiteboard = BooleanField('Whiteboard')
    cost = IntegerField('Cost per hour', validators=[DataRequired()])
    submit = SubmitField('Add Room')

class MeetingForm(FlaskForm):
    title = StringField('Meeting Title', validators=[DataRequired()])
    roomId = SelectField('Room', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    startTime = IntegerField('Start Time (24h format)', validators=[DataRequired()])
    duration = IntegerField('Duration (hours)', validators=[DataRequired()])
    submit = SubmitField('Book Meeting')

class TeamForm(FlaskForm):
    teamName = StringField('Team Name', validators=[DataRequired()])
    submit = SubmitField('Add Team')
