from flask import Blueprint, render_template, flash, request, url_for, redirect
# from flask_login import current_user
from database.database import get_db
from utility import RESTHub, ActivtityHistoryService, WalletService

bp = Blueprint('prices', __name__, url_prefix='/prices')


@bp.route('/', methods=['GET'])
def price_list():
    return render_template('prices/prices.html', data=RESTHub.get_current_data())


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
def modal(crypto_id):
    crypto = RESTHub.get_current_data_dict()[crypto_id]
    return render_template('prices/modal/modal.html', data=RESTHub.get_current_data(), crypto=crypto)


@bp.route('<crypto_id>', methods=['GET', 'POST'])
def add_crypto(crypto_id):
    db = get_db()
    data = request.form
    crypto = RESTHub.get_current_data_dict()[crypto_id]

    if request.method == 'POST':
        try:
            wallet = WalletService.find_wallet_asset_by(1, crypto_id)

            if not wallet:
                WalletService.insert(1, crypto_id, float(data['amount']) * crypto['current_price'])
            else:
                new_amount = float(wallet['amount']) + (float(data['amount']) * crypto['current_price'])
                WalletService.update(1, crypto_id, new_amount)
            ActivtityHistoryService.insert(1, crypto_id, (float(data['amount']) * crypto['current_price']), 1)

            db.commit()
        except db.Error as e:
            flash('There is some problem with database.', 'danger')
            print('DB Error: ' + str(e))
    flash('Successfully added new asset!', 'success')
    return redirect(url_for('wallet.wallet_list'))


@bp.route('/')
def introduction():
    return render_template('prices/prices.html')
