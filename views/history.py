from flask import Blueprint, render_template, flash
from database.database import get_db
from utility import RESTHub

bp = Blueprint('history', __name__, url_prefix='/history')


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

    return render_template('history/history.html', history_data=history_data, data_dict=RESTHub.get_current_data_dict())


@bp.route('/')
def introduction():
    return render_template('history/history.html')
