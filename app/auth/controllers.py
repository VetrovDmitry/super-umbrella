from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import datetime, time
from .models import db, User, Avatar
from app.chat.models import Member
from .forms import SignupForm, LoginForm, UploadAvatarForm, ChangeUsernameForm, ChangePasswordForm
import os


UPLOAD_DIR = 'app/static/uploads/'
SECOND_PATH = 'static/uploads/'

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.signup'))

        if form.password.data != form.repeat_password.data:
            flash('Passwords are not same')
            return redirect(url_for('auth.signup'))

        new_user_worksheet = {
            'email': form.email.data,
            'name': form.name.data,
            'username': form.username.data,
            'hash': generate_password_hash(form.password.data, method='sha256'),
            'date': datetime.datetime.now()
        }
        new_user = User(new_user_worksheet)
        db.session.add(new_user)
        db.session.commit()
        new_member = Member(new_user.id)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)


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
