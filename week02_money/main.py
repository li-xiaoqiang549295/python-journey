import sqlite3
import datetime
def get_conn():
    """打开数据库连接。文件不存在会自动创建。"""
    return sqlite3.connect("money.db")
def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            amount     REAL NOT NULL,
            category   TEXT NOT NULL,
            note       TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
def add(amount, category, note=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn()
    conn.execute(
        "INSERT INTO records "
        "(amount, category, note, created_at) "
        "VALUES (?, ?, ?, ?)",
        (amount, category, note, now)
    )
    conn.commit()
    conn.close()
    print(f"已记账：{amount} 元 - {category}")
def show(limit=10):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, amount, category, note, created_at FROM records ORDER BY id LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()

    if not rows:
        print("还没有记录")
        return

    for row in rows:
        rid, amount, category, note, created_at = row
        print(f"{rid}. {amount} 元 | {category} | {note} | {created_at}")
def main():
    init_db()
    print("=== 记账本 ===")
    print("add <金额> <分类> [备注] | list | quit")

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        parts = raw.split(maxsplit=3)
        cmd = parts[0].lower()

        if cmd == "add":
            if len(parts) < 3:
                print("用法：add 35 吃饭 午饭（备注可不填）")
                continue
            try:
                amount = float(parts[1])
            except ValueError:
                print("金额必须是数字，比如 add 35 吃饭")
                continue
            category = parts[2]
            note = parts[3] if len(parts) > 3 else ""
            add(amount, category, note)
        elif cmd == "list":
            show()
        elif cmd == "quit":
            print("再见")
            break
        else:
            print("未知命令，输入 add / list / quit")
if __name__ == "__main__":
    main()