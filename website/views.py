from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .api import get_nifty50, get_midcap_nifty, get_bank_nifty, get_fin_nifty

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.app_template_filter()
def numberFormat(value):
    return format(int(value), ',d')


@views.route('/midcpnifty')
@login_required
def midcpnifty():
    level, _data = get_midcap_nifty()
    return render_template("midcpnifty.html", user=current_user, data=_data, current_level=level, length=len(_data))


@views.route('/finnifty')
@login_required
def finnifty():
    level, _data = get_fin_nifty()
    return render_template("finnifty.html", user=current_user, data=_data, current_level=level, length=len(_data))


@views.route('/banknifty')
@login_required
def banknifty():
    level, _data = get_bank_nifty()
    print(len(_data))
    return render_template("banknifty.html", user=current_user, data=_data, current_level=level, length=len(_data))


@views.route('/nifty')
@login_required
def nifty():
    level, _data, expiry = get_nifty50()
    return render_template("nifty.html", user=current_user, data=_data, current_level=level, length=len(_data), expiry=expiry)
