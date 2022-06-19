import sqlite3
import pandas as pd
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


def find_by_user_id_as_df(user_id):
    cnx = sqlite3.connect('database/db.sqlite')
    df = pd.read_sql_query("SELECT * FROM activityHistory WHERE userId = ?", cnx, params=[user_id])
    cnx.commit()
    cnx.close()
    return df
