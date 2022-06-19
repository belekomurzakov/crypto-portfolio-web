from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user
from utility.User import User
from repositories import users
from database.database import get_db
from utility.auth import password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    db = get_db()

    try:
        user_data = users.find_user_by_id(user_id)
        if user_data is None:
            return None
        else:
            return User(user_data['id'], user_data['username'], user_data['isActive'] == 1)

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))
        return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must login first!', 'danger')
    return redirect(url_for('auth.login_form'))


@bp.get('/login')
def login_form():
    after_registration = request.args.get('after_registration')
    return render_template('login/login.html', data={}, after_registration=after_registration)


@bp.post('/login')
def login_action():
    db = get_db()
    data = request.form

    if 'username' not in data or 'password' not in data:
        flash('Fill a username and password!', 'error')
        return render_template('login/login.html', data=data)

    try:
        user_data = users.find_user_by_username_password(data['username'], password_hash(data['password']))

        if user_data is None:
            flash('You entered wrong credentials.', 'danger')
            return render_template('login/login.html', data=data)

        user = User(user_data['id'], user_data['username'], user_data['isActive'] == 1)
        login_user(user)
        return redirect(url_for('wallet.wallet_list'))

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))
        return render_template('login/login.html', data=data)


@bp.get('/registration')
def registration():
    return render_template('login/registration.html', data={})


@bp.post('/registration')
def register():
    db = get_db()
    data = request.form

    if 'username' not in data or len(data['username']) < 5 or 'password' not in data or len(data['password']) < 5:
        return render_template('login/registration.html',
                               error='Username should contain at least 5 symbols!',
                               data=data)
    print('Hash password: ' + password_hash(data['password']))

    try:
        users.insert(data['username'], password_hash(data['password']), data['firstName'], data['lastName'], 1)
        db.commit()
        flash('Success registration!', 'success')

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('auth.login_form', after_registration=True))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.introduction'))
