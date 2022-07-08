from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import datetime, time


main = Blueprint('main', __name__)


@main.route('/index')
def index():
    return render_template('main/index.html')