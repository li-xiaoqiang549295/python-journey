import logging
import pytest
from http_client import HttpClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-5s  %(name)s  %(message)s",
)

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def client():
    return HttpClient(BASE_URL)