from flask import Blueprint, render_template
bp = Blueprint('wallet', __name__, url_prefix='/wallet')


@bp.route('/')
def introduction():
    return render_template('wallet/wallet.html')
