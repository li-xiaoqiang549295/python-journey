![api-test](https://github.com/li-xiaoqiang549295/python-journey/actions/workflows/api-test.yml/badge.svg)

# python-journey

用 Python 从零开始做项目。每个项目都有完整代码、测试和文档。

## 项目

| 项目 | 内容 | 技术点 |
|---|---|---|
| [week01_todo](week01_todo/) | 命令行待办清单 | 文件持久化、函数拆分、模块化 |
| [week02_money](week02_money/) | 命令行记账本 | SQLite、SQL 分组统计、pytest 单元测试 |
| [week03_weather](week03_weather/) | 天气查询工具 | HTTP 请求、JSON 解析、缓存、异常处理 |
| [week04_api_test](week04_api_test/) | 接口自动化测试框架 | pytest、数据驱动、断言封装、GitHub Actions |

## 亮点：week04 接口自动化

- **16 条**用例，覆盖正常路径 / 异常路径 / 边界输入
- 用例写在 JSON 里，**加用例不用改代码**
- 请求、断言、日志三层封装
- 生成 HTML 报告，接入 GitHub Actions，**push 自动跑**

## 技术栈

Python 3.10 · SQLite · requests · pytest · pytest-html · GitHub Actions

## 怎么跑

```bash
# 命令行工具
cd week02_money && python main.py

# 单元测试
cd week02_money && pytest

# 接口测试
cd week04_api_test && pip install -r requirements.txt && pytest
```

## 学习记录

| 周次 | 内容 |
|---|---|
| 第 1 周 | Python 基础收尾 + 命令行待办清单 |
| 第 2 周 | 记账本：SQLite、SQL、拆模块 |
| 第 3 周 | 天气查询：HTTP、JSON、缓存 |
| 第 4 周 | 接口自动化测试框架 + CI |

## 方向

软件测试 / 测试开发
