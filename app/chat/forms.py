from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class CreateRoomForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    details = StringField('details', validators=[DataRequired()])
    submit = SubmitField('Create!')


class JoinRoomForm(FlaskForm):
    submit = SubmitField('Join!')


class LeaveRoomForm(FlaskForm):
    submit = SubmitField('Leave!')


class TextMessageForm(FlaskForm):
    content = StringField('content', validators=[DataRequired()])
    submit = SubmitField('Send!')