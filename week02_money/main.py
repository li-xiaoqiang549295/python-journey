import sqlite3
import datetime


def get_conn():
    """打开数据库连接。文件不存在会自动创建。"""
    return sqlite3.connect("money.db")