import pytest
import db


def test_add_and_count(temp_db):
    db.add(18,"吃饭","午饭")
    db.add(20,"玩","")
    conn = db.get_conn()
    count = conn.execute("select count(*) from records").fetchone()[0]
    conn.close()
    assert count == 2

def test_delete_and_count(temp_db):
    db.add(18,"吃饭","午饭")
    assert db.delete(1)==1
    assert db.delete(1)==0


def test_month_total_empty(temp_db):
    assert db.fetch_month_total("2026==12")==0

def test_month_total_only_counts_that_month(temp_db):
    conn = db.get_conn()
    conn.execute(
        "INSERT INTO records (amount, category, note, created_at) VALUES (?, ?, ?, ?)",
        (10, "吃饭", "", "2026-11-01 12:00:00"),
    )
    conn.execute(
        "INSERT INTO records (amount, category, note, created_at) VALUES (?, ?, ?, ?)",
        (99, "吃饭", "", "2026-10-01 12:00:00"),
    )
    conn.commit()
    conn.close()
    assert db.fetch_month_total("2026-11") == 10



def test_delete_nonexistent_returns_zero(temp_db):
    assert db.delete(999) == 0


def test_sqlite_does_not_check_type(temp_db):
    """SQLite 不校验类型：往 REAL 列插字符串不会报错。
    所以“金额必须是数字”的校验，必须在 Python 层做。"""
    db.add("abc", "吃饭")
    rows = db.fetch_recent()
    assert rows[0][1] == "abc"