import pytest
import db


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """每个测试一个独立的临时数据库。"""
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    return tmp_path

@pytest.fixture
def db_conn(temp_db):
    """提供一个连接，测试结束后自动关闭。"""
    conn = db.get_conn()
    yield conn
    conn.close()



