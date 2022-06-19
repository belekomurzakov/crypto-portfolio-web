from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from database.database import get_db
from repositories import activity, portfolio, cryptos
import json
import plotly
import plotly.express as px

bp = Blueprint('wallet', __name__, url_prefix='/wallet')


@bp.route('/', methods=['GET'])
@login_required
def wallet_list():
    wallet = portfolio.find_by_user_id(current_user.user_id)

    # graphs -start
    df = portfolio.find_by_user_id_as_df(current_user.user_id)
    fig = px.pie(df, values='amount', names='cryptoId')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    df = activity.find_by_user_id_as_df(current_user.user_id)
    line_fig = px.line(df, x='created', y="amount")
    line_json = json.dumps(line_fig, cls=plotly.utils.PlotlyJSONEncoder)
    # graphs -end

    return render_template('wallet/wallet.html',
                           wallet=wallet,
                           data_dict=cryptos.get_current_data_dict(),
                           graph_json=graph_json,
                           line_json=line_json)


@bp.route('/modal/<crypto_id>', methods=['GET', 'POST'])
@login_required
def modal(crypto_id):
    crypto = cryptos.get_current_data_dict()[crypto_id]
    wallet = portfolio.find_by_user_id(current_user.user_id)
    return render_template('wallet/modal/wallet-modal.html',
                           wallet=wallet,
                           data_dict=cryptos.get_current_data_dict(),
                           crypto=crypto)


@bp.route('<crypto_id>', methods=['GET', 'POST'])
def remove_crypto(crypto_id):
    db = get_db()
    data = request.form
    crypto = cryptos.get_current_data_dict()[crypto_id]

    if request.method == 'POST':
        try:
            wallet = portfolio.find_wallet_asset_by(current_user.user_id, crypto_id)

            if float(data['amount']) > wallet['amount']:
                flash('You don\'t have such an assets', 'danger')
                return redirect(url_for('wallet.wallet_list'))

            new_amount = float(wallet['amount']) - (float(data['amount']) * crypto['current_price'])
            portfolio.update(current_user.user_id, crypto_id, new_amount)
            activity.insert(current_user.user_id, crypto_id,
                            -(float(data['amount']) * crypto['current_price']), 0)

            db.commit()
        except db.Error as e:
            flash('There is some problem with database.', 'danger')
            print('DB Error: ' + str(e))

        flash('Successfully sold an asset', 'success')
    return redirect(url_for('wallet.wallet_list'))


@bp.route('/')
def introduction():
    return render_template('wallet/wallet.html')
