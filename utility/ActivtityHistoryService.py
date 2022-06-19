from database.database import get_db


def insert(user_id, crypto_id, amount, is_purchased):
    db = get_db()
    return db.execute("INSERT INTO activityHistory (userId, cryptoId, amount, isPurchased) "
                      "VALUES (?, ?, ?, ?)",
                      (user_id, crypto_id, amount, is_purchased)).lastrowid


def find_all():
    db = get_db()
    return db.execute("SELECT * FROM activityHistory").fetchall()


def find_by_user_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM activityHistory WHERE userId = ?", user_id).fetchall()
