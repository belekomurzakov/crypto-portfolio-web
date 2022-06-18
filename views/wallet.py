from flask import Blueprint, render_template, flash, request, url_for, redirect
# from flask_login import current_user
from database.database import get_db
from utility import RESTHub

bp = Blueprint('wallet', __name__, url_prefix='/wallet')


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
def modal(crypto_id):
    crypto = RESTHub.get_current_data_dict()[crypto_id]
    return render_template('wallet/modal/wallet-modal.html', data=RESTHub.get_current_data_dict(), crypto=crypto)


@bp.route('/', methods=['GET'])
def wallet_list():
    db = get_db()

    try:
        portfolio = db.execute("SELECT * "
                               "FROM wallet").fetchall()
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('wallet/wallet.html', portfolio=portfolio, data_dict=RESTHub.get_current_data_dict())


@bp.route('/')
def introduction():
    return render_template('wallet/wallet.html')
