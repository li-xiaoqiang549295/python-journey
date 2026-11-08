import sqlite3
import datetime


def get_conn():
    return sqlite3.connect("money.db")


def stat():
    month = datetime.datetime.now().strftime("%Y-%m")
    conn = get_conn()
    print(f"==={month}支出===:")
    row = conn.execute(
        "SELECT SUM(amount) FROM records WHERE created_at LIKE ?",
        (month + "%",),).fetchone()
    print(f"合计：{row[0] or 0}元")
    rows = conn.execute(
        "SELECT category, SUM(amount) FROM records "
        "WHERE created_at LIKE ? "
        "GROUP BY category "
        "ORDER BY SUM(amount) DESC",
        (month + "%",),
    ).fetchall()
    conn.close()
    for category, amount in rows:
        print(f"  {category}: {amount} 元")


def init_db():
    conn = get_conn()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS records
    (
    id         integer primary key autoincrement,
    amount     REAL NOT NULL,
    category   TEXT NOT NULL,
    note       TEXT NOT NULL,
    created_at TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def add(amount, category, note=""):
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_conn()
    conn.execute('''
    insert into records(amount, category, note,created_at) values (?, ?, ?, ?)
    ''', (amount, category, note, created_at))
    conn.commit()
    conn.close()
    print(f"已记账{amount},{category},{note}")


def show(limit=10):
    conn = get_conn()
    rows = conn.execute('''
    select id,amount,category,note,created_at from records order by id desc limit ?''',
                        (limit,)).fetchall()

    if not rows:
        print("还没有记录")
        return
    for row in rows:
        rid, amount, category, note, created_at = row
        print(f"{rid}. {amount}元|{category}|{note}|{created_at}")


def main():
    init_db()
    print("---------------记账本---------------")
    print("add 金额 用途 备注|list|stat|quit")
    while True:
        raw = input("请输入你的要求：").strip()
        if not raw:
            continue
        parts = raw.split(maxsplit=3)
        cmd = parts[0].lower()
        if cmd == "add":
            if len(parts) < 3:
                print("add 金额 用途 备注（可不写）")
                continue
            try:
                amount = float(parts[1])
            except ValueError:
                print("金额必须是数字")
                continue
            category = parts[2]
            note = parts[3] if len(parts) > 3 else ""
            add(amount, category, note)
        elif cmd == "list":
            show()
        elif cmd == "stat":
            stat()
        elif cmd == "quit":
            print("再见")
            break
        else:
            print("未知命令，请重新输入")


if __name__ == "__main__":
    main()

