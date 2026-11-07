import json


def load():
    """从 todos.json 读数据。文件不存在或是空的，都返回空列表。"""
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save(todos):
    """把 todos 写回 todos.json。todos 由调用方传进来。"""
    with open("todos.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
