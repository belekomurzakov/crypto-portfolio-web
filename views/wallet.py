from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from database.database import get_db
from utility import RESTHub, WalletService, ActivtityHistoryService

bp = Blueprint('wallet', __name__, url_prefix='/wallet')


@bp.route('/', methods=['GET'])
@login_required
def wallet_list():
    portfolio = WalletService.find_by_user_id(current_user.user_id)
    return render_template('wallet/wallet.html',
                           portfolio=portfolio,
                           data_dict=RESTHub.get_current_data_dict())


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
@login_required
def modal(crypto_id):
    crypto = RESTHub.get_current_data_dict()[crypto_id]
    portfolio = WalletService.find_by_user_id(current_user.user_id)
    return render_template('wallet/modal/wallet-modal.html',
                           portfolio=portfolio,
                           data_dict=RESTHub.get_current_data_dict(),
                           crypto=crypto)


@bp.route('<crypto_id>', methods=['GET', 'POST'])
def remove_crypto(crypto_id):
    db = get_db()
    data = request.form
    crypto = RESTHub.get_current_data_dict()[crypto_id]

    if request.method == 'POST':
        try:
            wallet = WalletService.find_wallet_asset_by(current_user.user_id, crypto_id)

            if float(data['amount']) > wallet['amount']:
                flash('You don\'t have such an assets', 'danger')
                return redirect(url_for('wallet.wallet_list'))

            new_amount = float(wallet['amount']) - (float(data['amount']) * crypto['current_price'])
            WalletService.update(current_user.user_id, crypto_id, new_amount)
            ActivtityHistoryService.insert(current_user.user_id, crypto_id,
                                           (float(data['amount']) * crypto['current_price']), 0)

            db.commit()
        except db.Error as e:
            flash('There is some problem with database.', 'danger')
            print('DB Error: ' + str(e))

        flash('Successfully sold an asset', 'success')
    return redirect(url_for('wallet.wallet_list'))


@bp.route('/')
def introduction():
    return render_template('wallet/wallet.html')
