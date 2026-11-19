import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

# 是否检查响应时间（默认关闭，因为跨境网络不稳定）
PERF_CHECK = os.getenv("PERF_CHECK", "0") == "1"
PERF_LIMIT = float(os.getenv("PERF_LIMIT", "5"))