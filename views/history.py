from flask import Blueprint, render_template
from repositories import activity, cryptos
from flask_login import login_required, current_user

bp = Blueprint('history', __name__, url_prefix='/history')


@bp.route('/', methods=['GET'])
@login_required
def history_list():
    history_data = activity.find_by_user_id(current_user.user_id)
    return render_template('history/history.html', history_data=history_data, data_dict=cryptos.get_current_data_dict())


@bp.route('/')
def introduction():
    return render_template('history/history.html')
