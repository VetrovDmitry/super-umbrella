from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import datetime, time
from . import models
from . import forms

from database import db
from app.chat.models import Member
import os


UPLOAD_DIR = 'app/static/uploads/'
SECOND_PATH = 'static/uploads/'


class UserController:
    def __init__(self):
        self.model = models.User

    def check_username_exists(self, username: str) -> dict:
        if self.model.find_by_username(username):
            return {'status': True, 'output': 'username: %s exists' % username}
        else:
            return {'status': False, 'output': 'username: %s does not exist' % username}

    def check_email_exists(self, email: str) -> dict:
        if self.model.find_by_email(email):
            return {'status': True, 'output': 'email: %s exists' % email}
        else:
            return {'status': False, 'output': 'email: %s does not exist' % email}

    def __new_user(self, name: str, username: str, email: str, password: str) -> int:
        hash = generate_password_hash(password, method='sha256')
        new_user = self.model(name=name,
                              username=username,
                              email=email,
                              hash=hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id

    def __new_member(self) -> int:
        return

    def create_user(self, user_data: dict) -> dict:
        new_user_id = self.__new_user(
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        return {'message': 'user %s was created' % new_user_id}



    def signup(self, user_data: dict) -> dict:
        new_user_id = self.__new_user(name=user_data['name'],
                              username=user_data['username'],
                              email=user_data['email'],
                              password=user_data['password'])

        db.session.add(Member(new_user_id))
        db.session.commit()
        return {'output': 'user %s signed up' % new_user_id}



auth = Blueprint('auth', __name__)


class Signup(MethodView):
    __controller = UserController()
    __form = forms.SignupForm
    __tamplate_name = 'auth/signup.html'

    def get(self):
        form = self.__form()
        return render_template(self.__tamplate_name, form=form)

    def post(self):
        form = self.__form()
        if form.validate_on_submit():
            if not form.check_passwords():
                flash('Passwords are different')
                return redirect(url_for('auth.signup'))

            user_data = form.data
            username_checking = self.__controller.check_username_exists(user_data['username'])
            if username_checking['status']:
                flash(username_checking['output'])
                return redirect(url_for('auth.signup'))

            email_checking = self.__controller.check_email_exists(user_data['email'])
            if email_checking['status']:
                flash(email_checking['output'])
                return redirect(url_for('auth.signup'))

            result = self.__controller.signup(user_data)
            flash(result['output'])
            return redirect(url_for('main.profile'))


auth.add_url_rule('/signup', view_func=Signup.as_view('signup'))


# @auth.route('/signup', methods=['POST', 'GET'])
# def signup():
#     form = SignupForm()
#
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             flash('Email address already exists')
#             return redirect(url_for('auth.signup'))
#
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             flash('Username already exists')
#             return redirect(url_for('auth.signup'))
#
#         if form.password.data != form.repeat_password.data:
#             flash('Passwords are not same')
#             return redirect(url_for('auth.signup'))
#
#         new_user_worksheet = {
#             'email': form.email.data,
#             'name': form.name.data,
#             'username': form.username.data,
#             'hash': generate_password_hash(form.password.data, method='sha256'),
#             'date': datetime.datetime.now()
#         }
#         new_user = User(new_user_worksheet)
#         db.session.add(new_user)
#         db.session.commit()
#         new_member = Member(new_user.id)
#         db.session.add(new_member)
#         db.session.commit()
#         return redirect(url_for('auth.login'))
#
#     return render_template('auth/signup.html', form=form)
# #
# #
@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('user with this email is not exist')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.hash, form.password.data):
            flash('Passowd not correct, please retry')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('auth.profile'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_data = user.min_info
    return render_template('auth/profile.html', data=user_data)


@auth.route('/settings')
@login_required
def settings():
    forms = {
        "change_username": ChangeUsernameForm(),
        "change_password": ChangePasswordForm(),
        "upload_avatar": UploadAvatarForm()
    }
    user = User.query.get(current_user.id)
    data = user.min_info
    return render_template('auth/settings.html', forms=forms, data=data)
