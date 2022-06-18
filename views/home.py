from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def introduction():
    return render_template('home/home.html')
