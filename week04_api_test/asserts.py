def assert_status(resp, expected):
    assert resp.status_code == expected, (
        f"状态码错误：期望 {expected}，实际 {resp.status_code}\n"
        f"响应内容：{resp.text[:300]}"
    )


def assert_fields(data, fields):
    """校验返回数据里包含指定字段。

    data 可能是单条（dict）或列表（list）。列表时校验第一条。
    """
    if not fields:
        return

    if isinstance(data, list):
        assert data, f"返回的是空列表，无法校验字段 {fields}"
        data = data[0]

    missing = [f for f in fields if f not in data]
    assert not missing, f"返回结果缺少字段：{missing}"


def assert_response_time(resp, max_seconds=5.0):
    assert resp.elapsed.total_seconds() < max_seconds, (
        f"响应太慢：{resp.elapsed.total_seconds():.2f}s > {max_seconds}s"
    )
