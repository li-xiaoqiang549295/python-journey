# 记账本（week02_money）

一个能真正用起来的命令行记账工具，数据存在本地 SQLite 数据库里。

## 进度

| 天 | 内容 | 状态 |
|---|---|---|
| Day 1 | 建表、记账、看流水 | ✅ |
| Day 2 | 本月合计 + 分类统计 | ✅ |
| Day 3 | 删除、输入校验、拆出 `db.py` | ✅ |
| Day 4 | 补文档、复盘 | ✅ |

## 功能

| 命令 | 例子 | 作用 |
|---|---|---|
| `add` | `add 35 吃饭 午饭` | 记一笔（金额 分类 备注） |
| `list` | `list` | 看最近 10 条，最新的在前 |
| `stat` | `stat` | 本月合计 + 按分类汇总 |
| `delete` | `delete 3` | 按 id 删除一条 |
| `quit` | `quit` | 退出 |

备注可以不填：`add 12 交通`。

## 项目结构

```
week02_money/
├── main.py     界面层：菜单、读输入、打印结果
├── db.py       数据层：建表、增删查
├── money.db    数据库文件（不进 Git）
└── README.md
```

**分层原则**：`db.py` 里不出现 `print`，只返回数据；`main.py` 不写 SQL。

## 运行

```bash
cd week02_money
python main.py
```

## 数据表

```sql
CREATE TABLE IF NOT EXISTS records (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    amount     REAL NOT NULL,
    category   TEXT NOT NULL,
    note       TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);
```

## 用到的知识

**Python**

- 函数的定义、参数、默认值、返回值
- 模块拆分与 `import`
- `try / except` 处理输入错误
- f-string 格式化（`{amount:.2f}`）
- 元组拆包
- `datetime` 取当前时间

**SQL / sqlite3**

- `connect / execute / commit / close`
- `INSERT`、`SELECT`、`DELETE`
- `WHERE ... LIKE` 按月过滤
- `GROUP BY` 分类汇总、`SUM`、`COUNT`
- `ORDER BY ... DESC`、`LIMIT`
- 参数化查询 `?`（防 SQL 注入）
- 主键与 `AUTOINCREMENT`
- `cursor.rowcount` 判断影响行数

## 复盘

### 卡最久的地方

（自己填：哪些地方反复出错、看了几遍才懂）

### 踩过的坑

1. `CREATE TABLE` 最后一个字段后面多了逗号 → `near ")": syntax error`
2. 建表改了字段名，但 `INSERT` 里还是旧的 → `table has no column named xxx`
3. `fetchone` 少写括号 → 打印出 `<built-in method fetchone ...>`
4. `execute()` 返回的是游标，没 `fetchall()` 就 `close()` → `Cannot operate on a closed database`
5. `SELECT` 字段数和拆包变量数不一致 → `too many/not enough values to unpack`
6. 同一秒写入的记录按 `created_at` 排序不稳定 → 改用 `id`

### 如果重写，会改什么

1. 用 `with` 语句管理数据库连接，异常时也能自动关闭
2. 金额用「分」为单位存整数，避免浮点误差
3. 加 `pytest` 单元测试，覆盖增删查的边界情况
4. 加 `update` 命令，支持修改已有记录

## 面试时怎么讲

> 这是我用 Python 写的一个命令行记账工具，数据存在 SQLite 里。
> 一开始单文件写完，后来拆成 `db.py` 和 `main.py` 两层，数据层不打印、界面层不写 SQL。
> SQL 全部用参数化查询，避免注入。
> 做完之后我把代码关掉，从零默写了一遍，顺便修了一个排序 bug：同一秒的记录按时间排序不稳定，改用自增 id。
