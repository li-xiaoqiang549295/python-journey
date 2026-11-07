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

todos = []  # 每个元素：{"text": "写代码", "done": False}


def add(text):
    """添加一条待办。TODO: 自己实现"""
    pass


def show():
    """列出全部，完成的显示 [x]，未完成显示 [ ]。TODO: 自己实现"""
    pass


def mark_done(index):
    """把第 index 条标记为完成（index 从 0 开始）。TODO: 自己实现"""
    pass


def delete(index):
    """删除第 index 条。TODO: 自己实现"""
    pass


def main():
    print("=== 待办清单 v0.1 ===")
    print("add <内容> | list | done <序号> | delete <序号> | quit")

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

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
