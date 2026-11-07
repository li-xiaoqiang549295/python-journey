"""待办清单 v0.1 —— 第 1 周练习

运行：python main.py

这是脚手架，函数体要你自己写。命令：
    add 写代码      添加一条
    list            列出全部
    done 1          把第 1 条标记完成
    delete 2        删除第 2 条
    quit            退出

Day 3：先把下面 4 个函数写出来（数据存在内存里）
Day 4：把 todos 存进 todos.json，重启不丢数据
Day 5：处理输入错误（比如 done abc）
Day 6：把存储逻辑拆到 storage.py
"""

import json

todos = []  # 每个元素：{"text": "写代码", "done": False}


def load():
    """从 todos.json 读数据。文件不存在就返回空列表。"""
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save():
    """把 todos 写回 todos.json。"""
    with open("todos.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add(text):
    if not text:
        print("内容不能为空")
        return
    todos.append({"text": text, "done": False})
    save()
    print(f"已添加：{text}")


def show():
    if not todos:
        print("还没有待办")
        return

    for i, t in enumerate(todos, start=1):
        mark = "x" if t["done"] else " "
        print(f"{i}. [{mark}] {t['text']}")


def mark_done(index):
    if 0 <= index < len(todos):
        todos[index]["done"] = True
        save()
        print(f"已完成：{todos[index]['text']}")
    else:
        print("序号不存在")


def delete(index):
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        save()
        print(f"已删除：{removed['text']}")
    else:
        print("序号不存在")


def main():
    global todos
    todos = load()
    print("=== 待办清单 v0.1 ===")
    print("add <内容> | list | done <序号> | delete <序号> | quit")

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        if cmd in ("done", "delete") and not arg.isdigit():
            print("请输入数字，比如 done 1")
            continue

        if cmd == "add":
            add(arg)
        elif cmd == "list":
            show()
        elif cmd == "done":
            mark_done(int(arg) - 1)
        elif cmd == "delete":
            delete(int(arg) - 1)
        elif cmd == "quit":
            print("再见")
            break
        else:
            print("未知命令，输入 add / list / done / delete / quit")


if __name__ == "__main__":
    main()
