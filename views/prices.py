from flask import Blueprint, render_template
bp = Blueprint('prices', __name__, url_prefix='/prices')


@bp.route('/')
def introduction():
    return render_template('prices/prices.html')
