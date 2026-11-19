# 接口自动化测试框架

基于 pytest + requests 的接口测试项目：用例用 JSON 描述，代码负责请求、断言、日志和报告。

## 覆盖范围

被测对象：`jsonplaceholder`（公开假数据接口）

| 类别 | 数量 | 内容 |
|---|---|---|
| 正常路径 | 9 | 增删改查、关联资源、条件筛选、分页 |
| 异常路径 | 4 | 资源不存在、非数字 id、负数 id、路径错误 |
| 边界/特殊输入 | 3 | 参数类型错误、空结果、超长字符串 |

## 目录结构

```
week04_api_test/
├── config.py        环境配置，BASE_URL 可用环境变量覆盖
├── http_client.py   HTTP 客户端封装：统一方法、超时、日志
├── asserts.py       断言封装：状态码、字段、响应时间
├── conftest.py      共享 fixture
├── data/posts.json  测试用例
├── test_posts.py    用例执行
└── pytest.ini       pytest 配置
```

## 快速开始

```bash
pip install -r requirements.txt

pytest                                              # 跑全部用例
pytest --html=report.html --self-contained-html     # 生成报告
python -m http.server 8000                          # 报告需用 http 打开
```

切换被测环境：

```bash
# Windows PowerShell
$env:BASE_URL="http://127.0.0.1:8000"
pytest
```

## 怎么加一条用例

只改 `data/posts.json`，**不用动任何 Python 代码**：

```json
{
  "name": "查询单篇文章",
  "method": "get",
  "path": "/posts/1",
  "expect_status": 200,
  "expect_fields": ["id", "title", "body"]
}
```

支持字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | 是 | 用例名，显示在报告里 |
| `method` | 是 | `get` / `post` / `put` / `delete` |
| `path` | 是 | 接口路径，如 `/posts/1` |
| `params` | 否 | URL 查询参数 |
| `body` | 否 | 请求体（JSON） |
| `expect_status` | 是 | 期望状态码 |
| `expect_fields` | 否 | 期望返回的字段 |
| `expect_len` | 否 | 期望返回的列表长度 |

## 设计说明


### 为什么封装 HttpClient
每个用例都要写 URL、超时、日志，重复度高。封装后改一处生效，
换环境只改 config.py 的 BASE_URL，用例不动。

### 为什么用例放 JSON
加用例不改代码；一个测试函数跑所有用例，代码量不随用例数增长；
用例是数据，非开发人员也能维护。

### 为什么断言单独封装
失败信息统一、判定标准集中、可复用。新增"响应时间校验"这类
通用断言时只写一次。

### 为什么性能断言可开关
功能测试求稳定，性能阈值随环境变化。混在一起会因网络抖动误报，
导致团队忽略红灯。默认关闭，需要时用 PERF_CHECK=1 打开。

## 踩坑记录

- 返回列表的接口，字段断言要取 `data[0]`，直接 `"key" in data` 是在找元素
- 用例里没有某个键时，`case["x"]` 会 `KeyError`，要用 `case.get("x")`
- `pytest-html` 生成的报告用 `file://` 打开时表格是空的，必须用 `http://` 访问
- 跨境访问接口偶尔 40 秒才返回，性能断言会误报，所以做成可开关
- 修改文件时把新代码“追加”到末尾，会导致代码重复或语法错误

## 后续计划

- 用 FastAPI 写一个真实服务，让这套框架测自己的服务
- 接入 GitHub Actions，push 自动跑测试
- 增加 Allure 报告