from flask import Blueprint, render_template, flash, request, url_for, redirect
from database.database import get_db
import requests
import json

bp = Blueprint('history', __name__, url_prefix='/history')


def get_current_data_dict():
    req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page'
                       '=250&page=1&sparkline=true&price_change_percentage=24h')
    data = json.loads(req.content)
    crypto_by_id = dict([(str(crypto['id']), crypto) for crypto in data])
    return crypto_by_id


@bp.route('/', methods=['GET'])
def history_list():
    db = get_db()

    try:
        history_data = db.execute("SELECT * "
                                  "FROM activityHistory").fetchall()
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))
    print('history_list after')

    return render_template('history/history.html', history_data=history_data, data_dict=get_current_data_dict())


@bp.route('/')
def introduction():
    return render_template('history/history.html')
