from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from application_files.model import User

class RegistrationForm(FlaskForm):
    """ Registration form"""

    username = StringField('username', validators=[InputRequired(message="Username required"),
                                       Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    email = StringField('Email',validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[InputRequired(message="Password required"),
                                         Length(min=4, max=25, message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField('Confirm password', validators=[InputRequired(message="Password required"),
                                                     EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """ Login form"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Password required")])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login Up')

class UpdateAccountForm(FlaskForm):
    """ Update Account form"""

    username = StringField('username', validators=[InputRequired(message="Username required"),
                                                   Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email :
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class SendMsgForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    receiver = StringField('To user:', validators=[InputRequired(message="Username required"),
                                       Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    content = TextAreaField('Contect', validators=[DataRequired()])
    submit = SubmitField('Send Message')

    def validate_receiver(self, receiver):
        receiverExist = (bool(User.query.filter_by(username=receiver.data).first()))
        if not receiverExist:
            raise ValidationError('That User dont exist. Please choose a registered user.')








    # def validate_username(self, username):
    #     user_object = User.query.filter_by(username=username.data).first()
    #     if user_object:
    #         raise ValidationError("Username already exists. Select a different username.")

# class LoginForm(FlaskForm):
#     """ Login form """
#
#     username = StringField('username', validators=[InputRequired(message="Username required")])
#     password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])

# def invalid_credentials(form, field):
#     """ Username and password checker """
#     username = form.username.data
#     password = field.data
#
#     # Check username is invalid
#     user_data = User.query.filter_by(username=username).first()
#     if user_data is None:
#         raise ValidationError("Username or password is incorrect")
#
#     # Check password in invalid
#     # elif not pbkdf2_sha256.verify(password, user_data.hashed_pswd):
#     #     raise ValidationError("Username or password is incorrect")
