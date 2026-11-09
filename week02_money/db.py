import sqlite3
import datetime


def get_conn():
    conn = sqlite3.connect('money.db')
    return conn


def init_db():
    conn = get_conn()
    conn.execute(''' 
    CREATE TABLE if not exists records( 
    id         integer primary key autoincrement,
    amount     REAL NOT NULL,
    category   TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()


def add(amount, category, note=""):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_conn()
    conn.execute('''
    INSERT INTO records (amount,category,note,created_at) VALUES (?,?,?,?) ''',
                 (amount, category, note, now), )
    conn.commit()
    conn.close()


def delete(rid):
    conn = get_conn()
    cur = conn.execute('''delete from records where id = ?''', (rid,), )
    conn.commit()
    conn.close()
    return cur.rowcount


def fetch_recent(limit=10):
    conn = get_conn()
    rows = conn.execute('''
    select id, amount, category, note, created_at from records
    order by id desc limit ?''', (limit,), ).fetchall()
    conn.close()
    return rows


def fetch_month_total(month):
    conn = get_conn()
    row = conn.execute('''select sum(amount) from records where created_at like ? 
    ''', (month + "%",), ).fetchone()
    conn.close()
    return row[0] or 0


def fetch_month_by_category(month):
    conn = get_conn()
    rows = conn.execute(
        "SELECT category, SUM(amount) FROM records "
        "WHERE created_at LIKE ? GROUP BY category ORDER BY SUM(amount) DESC",
        (month + "%",),
    ).fetchall()
    conn.close()
    return rows
