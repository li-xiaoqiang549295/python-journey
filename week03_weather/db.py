import datetime
import sqlite3


def get_conn():
    return sqlite3.connect("weather.db")


def init_db():
    conn = get_conn()
    conn.execute('''CREATE TABLE IF NOT EXISTS weather (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        city       TEXT NOT NULL,
        temp       TEXT NOT NULL,
        weather    TEXT NOT NULL,
        humidity   TEXT,
        queried_at TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

def save_log(city, today):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn()
    conn.execute(
        "insert into weather(city, temp, weather, humidity, queried_at)" "values(?,?,?,?,?)",
        (city, today["temp_C"], today["weatherDesc"][0]["value"], today["humidity"], now,))
    conn.commit()
    conn.close()


def get_cached(city, minutes=10):
    conn = get_conn()
    row = conn.execute("SELECT temp, weather, humidity ,queried_at from weather "
                       "where city = ? order by id desc limit 1"
                       , (city,),).fetchone()
    conn.close()
    if not row:
        return None
    temp, weather, humidity, queried_at = row
    last = datetime.datetime.strptime(queried_at, "%Y-%m-%d %H:%M:%S")
    if (datetime.datetime.now() - last).total_seconds() > minutes * 60:
        return None
    return temp, weather, humidity, queried_at


def fetch_history(limit=10):
    conn = get_conn()
    rows = conn.execute('''SELECT city, temp, weather, queried_at from weather 
    order by id desc limit ?''',
                        (limit,), ).fetchall()
    conn.close()
    return rows