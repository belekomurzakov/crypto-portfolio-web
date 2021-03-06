import sqlite3
import pandas as pd
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
    return db.execute("SELECT * FROM wallet WHERE amount > 0").fetchall()


def find_by_user_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM wallet WHERE userId = ? and amount > 0", user_id).fetchall()


def find_by_user_id_as_df(user_id):
    cnx = sqlite3.connect('database/db.sqlite')
    df = pd.read_sql_query("SELECT * FROM wallet WHERE userId = ?", cnx, params=[user_id])
    cnx.commit()
    cnx.close()
    return df
