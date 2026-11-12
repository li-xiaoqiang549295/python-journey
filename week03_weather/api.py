import requests


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