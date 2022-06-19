from database.database import get_db


def find_user_by_username_password(username, password):
    db = get_db()
    return db.execute("SELECT id, username, password, isActive FROM user WHERE username = ? AND password = ?",
                      (username, password)).fetchone()


def find_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT id, username, isActive FROM user WHERE id = ?", (user_id,)).fetchone()


def insert(username, password, first_name, last_name, is_active):
    db = get_db()
    return db.execute(
        "INSERT INTO user (username, password, firstName, lastName, isActive) VALUES (?, ?, ?, ?, ?)",
        (username, password, first_name, last_name, is_active)).lastrowid
