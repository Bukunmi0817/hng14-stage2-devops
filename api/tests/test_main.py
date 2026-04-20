import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

with patch('redis.Redis') as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis_fixture():
    with patch('main.r') as mock_r:
        mock_r.lpush = MagicMock()
        mock_r.hset = MagicMock()
        mock_r.hget = MagicMock(return_value="queued")
        yield mock_r

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_job(mock_redis_fixture):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36
    mock_redis_fixture.lpush.assert_called_once()
    mock_redis_fixture.hset.assert_called_once()

def test_get_job_found(mock_redis_fixture):
    mock_redis_fixture.hget.return_value = "queued"
    response = client.get("/jobs/test-job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"

def test_get_job_not_found(mock_redis_fixture):
    mock_redis_fixture.hget.return_value = None
    response = client.get("/jobs/nonexistent-job")
    assert response.status_code == 200
    assert response.json() == {"error": "not found"}

def test_create_job_returns_unique_ids(mock_redis_fixture):
    response1 = client.post("/jobs")
    response2 = client.post("/jobs")
    id1 = response1.json()["job_id"]
    id2 = response2.json()["job_id"]
    assert id1 != id2
