import sqlite3
from config import *


def add_user_to_db(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user (user_id, status) VALUES(?, ?)", (user_id, 0,))

    conn.commit()
    conn.close()


def check_user_exists(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id,))
    exists = bool(len(result.fetchall()))

    conn.close()

    return exists


def change_work_status(status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE bot_status SET status = ? WHERE operation = ?", (status, "Work_Status",))

    conn.commit()
    conn.close()


def get_bot_work_status():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT status FROM bot_status WHERE operation = ?", ("Work_Status",))
    result = result.fetchone()[0]

    conn.close()

    return result


def tstoo(proc):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO procedures (procedure) VALUES(?)", (proc,))

    conn.commit()
    conn.close()


def update_date_info(proc, av_dates):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE procedures SET av_dates = ? WHERE procedure = ?", (av_dates, proc,))

    conn.commit()
    conn.close()


def get_date_info(proc):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT av_dates FROM procedures WHERE procedure = ?", (proc,))
    result = result.fetchone()[0]

    conn.close()

    return result


def get_telegram_users():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user")
    result = result.fetchall()
    lst = [i[0] for i in result]

    conn.close()

    return lst


def get_usr_status(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT status FROM user WHERE user_id = ?", (user_id,))
    result = result.fetchone()[0]

    conn.close()

    return result


def change_user_status(status, user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET status = ? WHERE user_id = ?", (status, user_id,))

    conn.commit()
    conn.close()

