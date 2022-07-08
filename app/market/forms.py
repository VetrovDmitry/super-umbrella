from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email


class AddHouseForm(FlaskForm):
    city = StringField('city', validators=[DataRequired()])
    street = StringField('street', validators=[DataRequired()])
    house_number = StringField('house number' , validators=[DataRequired()])
    submit = SubmitField("To The Market")


class UploadPhotoForm(FlaskForm):
    image = FileField('photo', validators=[FileRequired(), FileAllowed(['png',
                                                                        'jpeg',
                                                                        'jpg'])])
    submit = SubmitField("upload")


class ChangeCostForm(FlaskForm):
    cost = FloatField("New Cost", validators=[DataRequired()])
    submit = SubmitField("Change")


class ChangeAddressForm(FlaskForm):
    city = StringField("New City", validators=[DataRequired()])
    street = StringField("New Street", validators=[DataRequired()])
    house_number = StringField("New House Number", validators=[DataRequired()])
    submit = SubmitField("Change")


class ChangeSummaryForm(FlaskForm):
    summary = StringField("New Summary", validators=[DataRequired()])
    submit = SubmitField("Change")
