from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import datetime, time
from .models import db, User, Avatar
from .forms import SignupForm, LoginForm, UploadAvatarForm, ChangeUsernameForm, ChangePasswordForm
import os


UPLOAD_DIR = 'app/static/uploads/'
SECOND_PATH = 'static/uploads/'

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
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
    avatar = Avatar.query.filter_by(user_id=current_user.id).first()
    avatar_path = 'uploads/' + avatar.path
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_data = {
        'username': user.username,
        'name': user.name,
        'date': str(user.date_registered).split(' ')[0],
        'email': user.email
    }
    return render_template('auth/profile.html', avatar=avatar_path, data=user_data)


@auth.route('/upload-avatar', methods=['POST', 'GET'])
@login_required
def upload_avatar():
    form = UploadAvatarForm()

    if form.validate_on_submit():
        f = form.avatar.data
        filename = str(int(time.time() * 1000)) + '.jpg'
        filename = secure_filename(filename)
        full_path = os.path.join(UPLOAD_DIR, filename)
        f.save(full_path)
        avatar = Avatar()
        avatar.user_id = current_user.id
        avatar.path = filename
        avatar.date_upload = datetime.datetime.now()
        db.session.add(avatar)
        db.session.commit()
        return redirect(url_for('auth.profile'))

    return render_template('auth/uploadavatar.html', form=form)


@auth.route('/index')
def index():
    return render_template('auth/index.html')


@auth.route('/settings')
def settings():
    return render_template('auth/settings.html')


@auth.route("/change-username", methods=['POST', 'GET'])
def change_username():
    form = ChangeUsernameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        user.username = form.new_username.data
        db.session.commit()
        return redirect(url_for('auth.profile'))

    return render_template("auth/changeusername.html", form=form)


@auth.route("/change-password")
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        user.hash = generate_password_hash(form.new_password.data, method='sha256')
        db.session.commit()
        return redirect(url_for("auth.profile"))

    return render_template("auth/changepassword.html", form=form)

@auth.route('/valuta')
def valuta():
    return render_template('auth/valuta.html')

