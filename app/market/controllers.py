from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from functools import wraps
from .models import db, House, Photo
from .forms import AddHouseForm, UploadPhotoForm, ChangeCostForm, ChangeAddressForm, ChangeSummaryForm


def house_required(func):
    @wraps(func)
    def decorated_view(house_id, *args, **kwargs):
        house = House.query.filter_by(id=house_id).first()
        if not house:
            return "House not on market"
        return func(house_id, *args, **kwargs)

    return decorated_view


def house_access_required(func):
    @wraps(func)
    def decorated_view(house_id, *args, **kwargs):
        house = House.query.filter_by(id=house_id).first()
        if house.user_id != current_user.id:
            return 'Have no access'
        return func(house_id, *args, **kwargs)

    return decorated_view


market = Blueprint("market", __name__)


@market.route("/market")
def marketplace():
    return render_template('market/index.html')


@market.route("/add-house", methods=['POST', 'GET'])
@login_required
def add_house():
    form = AddHouseForm()

    if form.validate_on_submit():
        # house = House.query.filter_by(
        #     city=form.city.data,
        #     street=form.street.data,
        #     house_number=form.house_number.data).first()
        # if house:
        #     flash("House with this address is already on market")
        #     return redirect(url_for("market.add_house"))

        new_house = House(city=form.city.data,
                          street=form.street.data,
                          house_number=form.house_number.data,
                          user_id=current_user.id)
        db.session.add(new_house)
        db.session.commit()
        return redirect(url_for('market.detail_house', house_id=new_house.id))

    return render_template("market/addhouse.html", form=form)


@market.route("/detail-house/<house_id>", methods=["POST", "GET"])
@login_required
@house_required
@house_access_required
def detail_house(house_id):
    # Все необходимые переменные для работы функции
    data = dict()
    current_house = House.query.get(house_id)

    forms = {
        'upload_image': UploadPhotoForm(),
        'change_cost': ChangeCostForm(),
        'change_address': ChangeAddressForm(),
        'change_summary': ChangeSummaryForm()
    }

    # Работа с формами
    if forms['change_cost'].validate_on_submit():
        current_house.cost = forms['change_cost'].cost.data
        db.session.commit()
        return redirect(url_for('market.detail_house', house_id=house_id))

    if forms['change_summary'].validate_on_submit():
        current_house.summary = forms['change_summary'].summary.data
        db.session.commit()
        return redirect(url_for('market.detail_house', house_id=house_id))


    data['house_info'] = current_house.get_min_info()
    return render_template('market/detailhouse.html', data=data, forms=forms)


@market.route("/house-details")
def house_details():
    return render_template("market/housedetails.html")