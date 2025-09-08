import os
import pytest
from fastapi.testclient import TestClient
from httpx import BasicAuth

from log_parser.main import app


@pytest.fixture(autouse=True)
def setup_env():
    os.environ.setdefault('NGINX_FILE_PATH', './tests/test_log.log')
    yield
    if 'NGINX_FILE_PATH' in os.environ:
        del os.environ['NGINX_FILE_PATH']


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_logs_with_real_file(client):
    response = client.get("/api/v1/get_metrics", auth=BasicAuth(client.app.state.config.api.login,
                                                                client.app.state.config.api.password))
    assert response.status_code == 200

    data = response.json()
    assert "response_statuses" in data
    assert isinstance(data["response_statuses"], dict)
    assert "average_time" in data
    assert isinstance(data["average_time"], float)
    assert "endpoints" in data
    assert isinstance(data["endpoints"], dict)
    assert "ips" in data
    assert isinstance(data["ips"], dict)
    assert "methods" in data
    assert isinstance(data["methods"], dict)
