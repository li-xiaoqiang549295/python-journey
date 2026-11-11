# 天气查询（week03_weather）

第 3 周项目：命令行天气查询工具，第一次用第三方库和网络请求。

## 功能

| 命令 | 例子 | 作用 |
|---|---|---|
| `weather` | `weather 北京` | 查一个城市的实时天气 |
| `history` | `history` | 看查过的记录 |
| `quit` | `quit` | 退出 |

## 3 天计划

| 天 | 内容 | 状态 |
|---|---|---|
| Day 1 | 装 `requests`，发出第一个请求，取出温度 | 进行中 |
| Day 2 | 封装 `fetch_weather()`，结果存进 SQLite，加 `history` | 未开始 |
| Day 3 | 缓存（10 分钟内不重复请求）、异常处理、拆文件 | 未开始 |

## 数据来源

接口：`https://wttr.in/<城市名>?format=j1`

- 不用注册、不用 API Key
- 支持中文城市名，比如 `北京`、`上海`
- 返回 JSON

抓取方式（Day 1 会写）：

```python
import requests

resp = requests.get("https://wttr.in/北京", params={"format": "j1"}, timeout=10)
data = resp.json()
```

**返回的 JSON 结构**（只列会用到的部分）：

```jsonc
{
  "current_condition": [          // 列表，只有 1 个元素
    {
      "temp_C": "9",              // 注意：是字符串，不是数字
      "humidity": "45",
      "windspeedKmph": "7",
      "weatherDesc": [            // 又是列表套字典
        { "value": "Sunny" }
      ]
    }
  ],
  "weather": [                    // 未来 3 天，每天一个元素
    { "date": "2026-11-10", "maxtempC": "15", "mintempC": "3" }
  ]
}
```

## 数据表（Day 2 用）

```sql
CREATE TABLE IF NOT EXISTS weather_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    city       TEXT NOT NULL,
    temp       TEXT NOT NULL,
    weather    TEXT NOT NULL,
    humidity   TEXT,
    queried_at TEXT NOT NULL
);
```

## 会学到的东西

- `pip install` 安装第三方库，理解虚拟环境
- HTTP 请求：GET、URL 参数、状态码
- JSON 与 Python 字典/列表的转换
- 网络异常的捕获（超时、断网、城市不存在）
- 缓存思想：同样的数据在有效期内不重复请求
- 沿用 Week 2 的分层结构（`db.py` + `main.py`）

## 踩坑记录

（边做边填）

- `temp_C` 是字符串，参与计算要先 `float()`
- 城市名拼错时接口返回 HTTP 500，不是 404
- 没有 `timeout` 参数时，网络卡住会让程序永远停着
