def assert_status(resp, expected):
    assert resp.status_code == expected, (
        f"状态码错误：期望 {expected}，实际 {resp.status_code}\n"
        f"响应内容：{resp.text[:300]}"
    )


def assert_fields(data, fields):
    if not fields:
        return
    missing = [f for f in fields if f not in data]
    assert not missing, f"返回结果缺少字段：{missing}"


def assert_response_time(resp, max_seconds=2.0):
    assert resp.elapsed.total_seconds() < max_seconds, (
        f"响应太慢：{resp.elapsed.total_seconds():.2f}s > {max_seconds}s"
    )