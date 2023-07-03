from fastapi.testclient import TestClient

from jwt_service.main import app


client = TestClient(app)
