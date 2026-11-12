from db import (init_db,save_log,get_cached,fetch_history)
from api import get_weather


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
    print(f"=== {city} ===")
    print(f"温度：{today['temp_C']} ℃")
    print(f"天气：{today['weatherDesc'][0]['value']}")
    print(f"湿度：{today['humidity']}%")
    print(f"风速：{today['windspeedKmph']} km/h")
    print("--- 未来三天 ---")
    for day in data["weather"]:
        print(f"{day['date']}   {day['mintempC']} ~ {day['maxtempC']} ℃")
    save_log(city, today)


def show_history(limit=10):
    rows = fetch_history(limit)
    if not rows:
        print("还没有记录")
        return
    for city,temp,weather,queried_at in rows:
        print(f"{city} {temp} {weather} {queried_at}")

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
