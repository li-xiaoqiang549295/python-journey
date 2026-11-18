import logging
import requests

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        """所有请求都走这里，日志和超时只写一次。"""
        url = self.base_url + path
        logger.info("请求 %s %s", method.upper(), url)

        resp = self.session.request(method, url, timeout=10, **kwargs)

        logger.info("响应 %s | %s 字节 | %s", resp.status_code, len(resp.text), url)
        return resp

    def get(self, path, **kwargs):
        return self.request("get", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("post", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("put", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("delete", path, **kwargs)