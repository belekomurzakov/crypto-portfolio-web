"""
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user

from utility.User import User
from database.database import get_db
from utility.auth import password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    db = get_db()

    try:
        user_data = db.execute(
            "SELECT id, username, active FROM user WHERE id = ?",
            (user_id,)
        ).fetchone()

        if user_data is None:
            return None
        else:
            return User(user_data['id'], user_data['username'], user_data['active'] == 1, user_data['userRole'])

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))
        return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must login first!', 'error')
    return redirect(url_for('auth.login_form'))


@bp.get('/login')
def login_form():
    after_registration = request.args.get('after_registration')
    return render_template('auth/login.html', data={}, after_registration=after_registration)


@bp.post('/login')
def login_action():
    db = get_db()
    data = request.form

    if 'username' not in data or 'password' not in data:
        flash('Vyplňte prosím přihlašovací jméno a heslo!', 'error')
        return render_template('auth/login.html', data=data)

    try:
        user_data = db.execute(
            "SELECT id, username, password, active, userRole "
            "FROM user "
            "WHERE username = ? AND password = ?",
            (data['username'], password_hash(data['password']))
        ).fetchone()

        if user_data is None:
            flash('Zadali jste nesprávné přihlašovací údaje.', 'error')
            return render_template('auth/login.html', data=data)

        user = User(user_data['id'], user_data['username'], user_data['active'] == 1, user_data['userRole'])
        login_user(user)
        return redirect(url_for('companies.partner_list'))

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))
        return render_template('auth/login.html', data=data)


@bp.get('/registration')
def registration():
    return render_template('auth/registration.html', data={})


@bp.post('/registration')
def register():
    db = get_db()
    data = request.form

    if (
            'username' not in data or len(data['username']) < 5 or
            'password' not in data or len(data['password']) < 5
    ):
        return render_template('auth/registration.html',
                               error='Uživatelské jméno musí mít minimálně 5 znaků!',
                               data=data)

    print('Zahashované heslo: ' + password_hash(data['password']))

    try:
        birthdate_timestamp = (datetime.timestamp(datetime.strptime(data['birthdate'], '%Y-%m-%d')) * 1000)

        new_id = db.execute(
            "INSERT INTO user (username, password, firstName, lastName, "
            "userRole, mobile, street, city, country, birthdate, active) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (data['username'], password_hash(data['password']), data['firstName'], data['lastName'], data['role'],
             data['phone'], data['street'], data['city'], data['country'], birthdate_timestamp, 1)
        ).lastrowid
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
    return redirect(url_for('homepage.introduction'))
"""