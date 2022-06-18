from flask import Blueprint, render_template

bp = Blueprint('prices', __name__, url_prefix='/prices')
import requests
import json


@bp.route('/', methods=['GET'])
def get_data():
    req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page'
                       '=250&page=1&sparkline=true&price_change_percentage=24h')
    data = json.loads(req.content)
    return render_template('prices/prices.html', data=data)


@bp.route('/')
def introduction():
    return render_template('prices/prices.html')
