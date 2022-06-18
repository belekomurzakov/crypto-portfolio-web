from flask import Blueprint, render_template, flash, request, url_for, redirect
# from flask_login import current_user
from database.database import get_db
from utility import RESTHub

bp = Blueprint('prices', __name__, url_prefix='/prices')


@bp.route('/', methods=['GET'])
def price_list():
    return render_template('prices/prices.html', data=RESTHub.get_current_data())


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
def modal(crypto_id):
    crypto = RESTHub.get_current_data_dict()[crypto_id]
    return render_template('prices/modal/modal.html', data=RESTHub.get_current_data(), crypto=crypto)


@bp.route('<crypto_id>', methods=['GET', 'POST'])
def insert(crypto_id):
    db = get_db()
    data = request.form
    crypto = RESTHub.get_current_data_dict()[crypto_id]

    if request.method == 'POST':
        try:
            wallet = db.execute("SELECT id, amount "
                                "FROM wallet WHERE cryptoId = ? AND userId = ?", (crypto_id, 1)).fetchall()
            if not wallet:
                new_id = db.execute("INSERT INTO wallet (userId, cryptoId, amount) "
                                    "VALUES (?, ?, ?)",
                                    (1, crypto_id, float(data['amount']) * crypto['current_price'])).lastrowid
                db.commit()
                return redirect(url_for('wallet.wallet_list'))

            new_amount = float(wallet[0]['amount']) + (float(data['amount']) * crypto['current_price'])

            db.execute("UPDATE wallet SET cryptoId = ?, amount = ? WHERE userId = ? and cryptoId = ?",
                       (crypto_id, new_amount, 1, crypto_id))

            inserted_id = db.execute("INSERT INTO activityHistory (userId, cryptoId, amount, isPurchased) "
                                     "VALUES (?, ?, ?, ?)",
                                     (1, crypto_id, float(data['amount']) * crypto['current_price'], 1)).lastrowid

            db.commit()
        except db.Error as e:
            flash('There is some problem with database.', 'error')
            print('DB Error: ' + str(e))

    return redirect(url_for('wallet.wallet_list'))


@bp.route('/')
def introduction():
    return render_template('prices/prices.html')
