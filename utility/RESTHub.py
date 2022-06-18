import requests
import json


def get_current_data():
    req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page'
                       '=250&page=1&sparkline=true&price_change_percentage=24h')
    data = json.loads(req.content)
    return data


def get_current_data_dict():
    crypto_by_id = dict([(str(crypto['id']), crypto) for crypto in get_current_data()])
    return crypto_by_id
