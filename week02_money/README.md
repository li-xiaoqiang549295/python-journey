# 记账本（week02_money）

第 2 周项目：一个能真正用起来的命令行记账工具。

## 进度

| 天 | 内容 | 状态 |
|---|---|---|
| Day 1 | 建表、记账、看流水 | ✅ 完成 |
| Day 2 | 本月统计（`stat`） | 未开始 |
| Day 3 | 删除、输入校验、拆文件 | 未开始 |
| Day 4 | 收尾、复盘 | 未开始 |

## 命令

| 命令 | 例子 | 作用 |
|---|---|---|
| `add` | `add 35 吃饭 午饭` | 记一笔（金额 分类 备注） |
| `list` | `list` | 看最近 10 条 |
| `quit` | `quit` | 退出 |

备注可以不填：`add 12 交通`。

## 数据表

```sql
CREATE TABLE IF NOT EXISTS records (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    amount     REAL NOT NULL,
    category   TEXT NOT NULL,
    note       TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
```

## 运行

```bash
cd week02_money
python main.py
```

## 日志

- 2026-11-07：Day 1 完成，能建表、记账、看流水。

## 进阶思考

- 金额用 `float` 存，`0.1 + 0.2` 会得到 `0.30000000000000004`。真实项目用「分」为单位存整数。
- SQL 里永远不要用 f-string 拼参数，一律用 `?` 占位符，否则会被 SQL 注入。
- `money.db` 是二进制文件，不要用编辑器打开，也不应该提交到 Git。
