import datetime
from db import (
    init_db, add, delete,
    fetch_recent, fetch_month_total, fetch_month_by_category,
)


def stat():
    month = datetime.datetime.now().strftime("%Y-%m")
    total = fetch_month_total(month)
    rows = fetch_month_by_category(month)
    print(f"=== {month}支出 ===")
    print(f"合计:{total} 元")
    if not rows:
        print("还没有记录")
        return
    for category, amount in rows:
        print(f"{category}: {amount} 元")


def show(limit=10):
    rows = fetch_recent(limit)
    if not rows:
        print("还没有记录")
        return
    for rid, amount, category, note, created_at in rows:
        print(f"{rid}. {amount:.2f} 元 | {category} | {note} | {created_at}")


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
            print(f"已记账：{amount} 元 - {category}")
        elif cmd == "list":
            show()
        elif cmd == "stat":
            stat()
        elif cmd == "delete":
            if len(parts) < 2 or not parts[1].isdigit():
                print("用法：delete 3（3 是 list 里显示的 id）")
                continue
            deleted = delete(int(parts[1]))
            if deleted == 0:
                print("没有这条记录")
            else:
                print("已删除")
        elif cmd == "quit":
            print("再见")
            break
        else:
            print("未知命令，请重新输入")


if __name__ == "__main__":
    main()
