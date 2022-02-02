from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import db, House, Photo
from .forms import AddHouseForm, UploadPhotoForm


market = Blueprint("market", __name__)


@market.route("/market")
def marketplace():
    return render_template('market/index.html')


@market.route("/add-house", methods=['POST', 'GET'])
def add_house():
    form = AddHouseForm()

    return render_template("market/addhouse.html", form=form)


@market.route("/house-details")
def house_details():
    return render_template("market/housedetails.html")