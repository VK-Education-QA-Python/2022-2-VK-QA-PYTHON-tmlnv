import pytest
from application.fastapi_app import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.FastAPI
class TestServer:

    def test_read_main(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_add_get_user(self):
        resp = client.post('/add_user', json={'name': 'Artem'})
        user_id_from_add = resp.json()['user_id']

        resp = client.get('/get_user/Artem')
        user_id_from_get = resp.json()['user_id']

        assert user_id_from_add == user_id_from_get

    def test_add_existent_user(self):
        client.post('/add_user', json={'name': 'Arima'})
        resp = client.post('/add_user', json={'name': 'Arima'})

        assert resp.status_code == 400

    def test_get_non_existent_user(self):
        resp = client.get('get_user/Tyler')

        assert resp.status_code == 404
