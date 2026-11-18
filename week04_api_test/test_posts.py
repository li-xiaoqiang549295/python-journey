import json
import os
import pytest
from asserts import assert_status, assert_fields, assert_response_time

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "posts.json")

with open(DATA_FILE, encoding="utf-8") as f:
    CASES = json.load(f)


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_api(client, case):
    kwargs = {}
    if "params" in case:
        kwargs["params"] = case["params"]
    if "body" in case:
        kwargs["json"] = case["body"]

    resp = getattr(client, case["method"])(case["path"], **kwargs)

    assert_status(resp, case["expect_status"])
    assert_response_time(resp, 3.0)

    if case["expect_fields"]:
        assert_fields(resp.json(), case["expect_fields"])