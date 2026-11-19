import logging
import pytest
from http_client import HttpClient
from config import BASE_URL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-5s  %(name)s  %(message)s",
)


@pytest.fixture
def client():
    return HttpClient(BASE_URL)