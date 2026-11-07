# 记账本（week02_money）

第 2 周项目：一个能真正用起来的命令行记账工具。

## 做什么

记录每天花了多少钱，随时查看流水，月底知道钱花在哪了。

## 命令

| 命令 | 例子 | 作用 |
|---|---|---|
| `add` | `add 35 吃饭 午饭` | 记一笔（金额 分类 备注） |
| `list` | `list` | 看最近 10 条 |
| `stat` | `stat` | 本月总支出 + 按分类汇总 |
| `delete` | `delete 3` | 删除第 3 条 |
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

## 4 天计划

### Day 1：建库 + 记账 + 看账
- 学会 `sqlite3` 的连接、执行、提交
- `init_db()`：建表
- `add()`：插入一条
- `list`：查询最近 10 条并打印

**验收**：`add 35 吃饭 午饭` → `add 12 交通` → `list` 看到两行；退出重进还在。

### Day 2：统计
- `stat`：本月合计 + 每个分类的合计
- 用到 SQL 的 `WHERE`（按月份过滤）和 `GROUP BY`（按分类汇总）

**验收**：`stat` 输出本月总额和“吃饭 35 元、交通 12 元”。

### Day 3：删除 + 输入校验 + 拆文件
- `delete 3`：按 id 删除
- 金额不是数字、序号不存在时不崩
- 拆成 `db.py`（数据库操作）+ `main.py`（界面）

**验收**：`add abc 吃饭` 只提示不崩；`delete 999` 提示不存在。

### Day 4：收尾
- 写 README（这个文件就是）
- 录 1 分钟演示
- 复盘：卡在哪、怎么解决

## 每天收工

```powershell
git add .
git commit -m "week02 day1: 建表和记账"
git push
```

## 进阶思考（做完再看）

- 金额用 `float` 存，`0.1 + 0.2` 会得到 `0.30000000000000004`。真实项目用「分」为单位存整数。
- SQL 里永远不要用 f-string 拼参数，一律用 `?` 占位符，否则会被 SQL 注入。
