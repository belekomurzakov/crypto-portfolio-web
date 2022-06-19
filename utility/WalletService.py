from database.database import get_db


def find_wallet_asset_by(user_id, crypto_id):
    db = get_db()
    return db.execute("SELECT id, amount FROM wallet WHERE cryptoId = ? AND userId = ?",
                      (crypto_id, user_id)).fetchone()


def insert(user_id, crypto_id, amount):
    db = get_db()
    return db.execute("INSERT INTO wallet (userId, cryptoId, amount) "
                      "VALUES (?, ?, ?)",
                      (user_id, crypto_id, amount)).lastrowid


def update(user_id, crypto_id, amount):
    db = get_db()
    return db.execute("UPDATE wallet SET cryptoId = ?, amount = ? WHERE userId = ? and cryptoId = ?",
                      (crypto_id, amount, user_id, crypto_id))


def find_all():
    db = get_db()
    return db.execute("SELECT * FROM wallet").fetchall()


def find_by_user_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM wallet WHERE userId = ?", user_id).fetchall()
