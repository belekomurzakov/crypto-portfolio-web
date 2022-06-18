from flask import Blueprint, render_template, flash, request, url_for, redirect
# from flask_login import current_user
from database.database import get_db
import requests
import json

bp = Blueprint('prices', __name__, url_prefix='/prices')


def get_current_data():
    req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page'
                       '=250&page=1&sparkline=true&price_change_percentage=24h')
    data = json.loads(req.content)
    return data


def get_current_data_dict():
    crypto_by_id = dict([(str(crypto['id']), crypto) for crypto in get_current_data()])
    return crypto_by_id


@bp.route('/', methods=['GET'])
def price_list():
    return render_template('prices/prices.html', data=get_current_data())


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
def modal(crypto_id):
    crypto = get_current_data_dict()[crypto_id]
    return render_template('prices/modal/modal.html', data=get_current_data(), crypto=crypto)


@bp.route('<crypto_id>', methods=['GET', 'POST'])
def insert(crypto_id):
    db = get_db()
    data = request.form
    crypto = get_current_data_dict()[crypto_id]

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
