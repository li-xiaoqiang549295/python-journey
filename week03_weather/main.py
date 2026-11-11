import requests
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


def get_weather(city):
    try:
        url = f"https://wttr.in/{city}"
        resp = requests.get(url, params={"format": "j1"}, timeout=10)
    except requests.Timeout:
        print("请求连接超时，连接可能不稳")
        return None
    except requests.ConnectionError:
        print("连接失败，检查一下网络")
        return None
    if resp.status_code != 200:
        return None
    return resp.json()


def show_history(limit=10):
    conn = get_conn()
    rows = conn.execute('''SELECT city, temp, weather, queried_at from weather 
    order by id desc limit ?''',
                        (limit,), ).fetchall()
    if not rows:
        print("还没有记录")
        return
    for city, temp, weather, queried_at in rows:
        print(f"{city},{temp},{weather},{queried_at}")
    conn.close()


def show_weather(city):
    cached = get_cached(city)
    if cached:
        temp, weather, humidity, queried_at = cached
        print(f"=== {city} ===（{queried_at} 的缓存）")
        print(f"温度：{temp} ℃")
        print(f"天气：{weather}")
        print(f"湿度：{humidity}%")
        return
    data = get_weather(city)
    if data is None:
        print(f"查不到「{city}」的天气，检查一下城市名")
        return
    today = data["current_condition"][0]
    print(f"==={city}===")
    print(f"温度：{today['temp_C']} ℃")
    print(f"天气：{today['weatherDesc'][0]['value']}")
    print(f"湿度：{today['humidity']}%")
    print(f"风速：{today['windspeedKmph']} km/h")
    print("--- 未来三天 ---")
    for day in data["weather"]:
        print(f"{day['date']}   {day['mintempC']} ~ {day['maxtempC']} ℃")
    save_log(city, today)


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


def main():
    init_db()
    while True:
        row = input("请输入你要进行的操作:").strip()
        if not row:
            continue
        parts = row.split(maxsplit=1)
        cmd = parts[0].lower()
        if cmd == "weather":
            if len(parts) < 2:
                print("注意格式weather city")
                continue
            show_weather(parts[1])
        elif cmd == "history":
            show_history()
        elif cmd == "quit":
            break
        else:
            print("未知命令：weather / history / quit")


if __name__ == "__main__":
    main()
