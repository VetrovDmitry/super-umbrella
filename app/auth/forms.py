from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('repeat password', validators=[DataRequired()])
    submit = SubmitField('send')

    def check_passwords(self) -> bool:
        if self.repeat_password != self.password:
            return False
        else:
            return True

    @property
    def data(self) -> dict:
        return {
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }


class LoginForm(FlaskForm):
    email = StringField("email", validators=[Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("send")


class UploadAvatarForm(FlaskForm):
    avatar = FileField('avatar', validators=[FileRequired()])
    submit = SubmitField('upload')


class ChangeUsernameForm(FlaskForm):
    new_username = StringField("new username", validators=[DataRequired()])
    submit = SubmitField("change")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("new password", validators=[DataRequired()])
    submit = SubmitField("change")