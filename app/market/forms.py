from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email


class AddHouseForm(FlaskForm):
    city = StringField('city', validators=[DataRequired()])
    street = StringField('street', validators=[DataRequired()])
    house_number = StringField('house number' , validators=[DataRequired()])
    summary = StringField('summary' , validators=[DataRequired()])
    cost = FloatField('cost' , validators=[DataRequired()])
    submit = SubmitField("To The Market")


class UploadPhotoForm(FlaskForm):
    image = FileField('photo', validators=[FileRequired(), FileAllowed(['png',
                                                                        'jpeg',
                                                                        'jpg'])])
    submit = SubmitField("upload")


