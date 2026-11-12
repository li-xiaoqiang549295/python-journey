# 天气查询（week03_weather）

命令行天气查询工具：查实时天气，缓存结果，记录历史。

## 进度

| 天 | 内容 | 状态 |
|---|---|---|
| Day 1 | 装 `requests`、发 HTTP 请求、解析 JSON | ✅ |
| Day 2 | 菜单、查询记录入库、history | ✅ |
| Day 3 | 缓存（10 分钟 TTL）、网络异常处理 | ✅ |
| Day 4 | 拆出 `api.py` / `db.py`、补文档 | ✅ |

## 功能

| 命令 | 例子 | 作用 |
|---|---|---|
| `weather` | `weather 北京` | 查实时天气 + 未来三天 |
| `history` | `history` | 看最近 10 次查询 |
| `quit` | `quit` | 退出 |

## 项目结构

```
week03_weather/
├── main.py     界面层：菜单、打印、流程控制
├── api.py      网络层：请求 wttr.in，解析 JSON
├── db.py       数据层：SQLite 读写、缓存判断
└── README.md
```

**分层的规矩**：

- `api.py` 不发 `print`，失败返回 `None`
- `db.py` 不发 `print`，只返回数据
- `main.py` 负责所有输出

## 运行

```bash
pip install requests
cd week03_weather
python main.py
```

## 数据来源

`https://wttr.in/<城市>?format=j1`

- 免费、不用 API Key
- 支持中文城市名
- 城市名写错时返回 **HTTP 500**（不是 404）
- 服务偶尔不稳定，会连接失败或超时

## 数据表

```sql
CREATE TABLE IF NOT EXISTS weather (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    city       TEXT NOT NULL,
    temp       TEXT NOT NULL,
    weather    TEXT NOT NULL,
    humidity   TEXT,
    queried_at TEXT NOT NULL
);
```

`weather.db` 是运行时产物，已加入 `.gitignore`。

## 缓存逻辑

查询前先看数据库里这个城市**最新的一条**记录：

- 距现在 < 10 分钟 → 直接用，不发请求
- 否则（或没有记录）→ 请求接口，成功后写入

判断“最新一条”必须写 `ORDER BY id DESC LIMIT 1`，否则拿到的是最老的记录。

## 用到的知识

**网络**

- HTTP GET、URL 参数、状态码
- `timeout` 的作用
- `requests.Timeout` / `ConnectionError` 的区别
- JSON 与 Python 字典/列表的互转

**Python**

- `pip` 安装第三方库、虚拟环境
- 模块拆分（三层结构）
- `datetime.strptime` 解析时间、`total_seconds()` 算差值
- 元组拆包、早返回（early return）

**数据库**

- 沿用 Week 2 的 SQLite 套路
- 缓存 TTL 的实现思路

## 复盘

### 踩坑记录

1. `temp_C` 是字符串，`weatherDesc` 是列表套字典，要 `[0]["value"]` 才能取到
2. 城市名拼错时接口返回 500，不是 404
3. 没有 `timeout`，网络卡住程序会永远停着
4. 缓存查询忘了 `ORDER BY id DESC LIMIT 1`，永远拿到最老的记录，缓存形同虚设
5. 改了函数返回值数量，忘了改调用处的拆包 → `too many/not enough values to unpack`
6. `db.py` 里写 `print` 破坏分层，`history` 变成在数据层打印

### 如果重写，会改什么

1. 加失败重试（`for _ in range(2)`）
2. 缓存存完整 JSON，连“未来三天”一起缓存
3. 用 `with` 管理数据库连接
4. 加单元测试：解析函数用固定的 JSON 样本测试，不依赖网络

## 面试时怎么讲

> 这是我用 Python 做的一个天气查询工具，数据来自 wttr.in 的公开接口。
> 项目分三层：`api.py` 负责请求和解析，`db.py` 负责 SQLite，`main.py` 负责交互。
> 做了两级容错：网络层捕获超时和断连，业务层判断空结果。
> 加了 10 分钟缓存，查同一个城市不会重复请求，缓存判断用的 `ORDER BY id DESC LIMIT 1`。
> 中途踩过一个坑：改了 `get_cached` 的返回值，忘了同步改调用方的拆包，报 `too many values to unpack`——从那以后我改函数签名都会先搜一遍调用点。
