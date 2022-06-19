from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from database.database import get_db
from repositories import activity, cryptos, portfolio

bp = Blueprint('prices', __name__, url_prefix='/prices')


@bp.route('/', methods=['GET'])
def price_list():
    return render_template('prices/prices.html', data=cryptos.get_current_data())


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
@login_required
def modal(crypto_id):
    crypto = cryptos.get_current_data_dict()[crypto_id]
    return render_template('prices/modal/modal.html', data=cryptos.get_current_data(), crypto=crypto)


@bp.route('<crypto_id>', methods=['GET', 'POST'])
def add_crypto(crypto_id):
    db = get_db()
    data = request.form
    crypto = cryptos.get_current_data_dict()[crypto_id]

    if request.method == 'POST':
        try:
            wallet = portfolio.find_wallet_asset_by(current_user.user_id, crypto_id)

            if not wallet:
                portfolio.insert(current_user.user_id, crypto_id, float(data['amount']) * crypto['current_price'])
            else:
                new_amount = float(wallet['amount']) + (float(data['amount']) * crypto['current_price'])
                portfolio.update(current_user.user_id, crypto_id, new_amount)
            activity.insert(current_user.user_id, crypto_id,
                            (float(data['amount']) * crypto['current_price']), 1)

            db.commit()
        except db.Error as e:
            flash('There is some problem with database.', 'danger')
            print('DB Error: ' + str(e))
    flash('Successfully added new asset!', 'success')
    return redirect(url_for('wallet.wallet_list'))


@bp.route('/')
def introduction():
    return render_template('prices/prices.html')
