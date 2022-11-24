import os
import pytest
import requests
import settings
import json

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


@pytest.fixture()
def save_file_surname_root(repo_root_fix):
    return os.path.join(repo_root_fix, 'tmp', 'save.json')


@pytest.mark.FastAPI
class TestFastApiComplicated:
    def test_from_outside(self):
        res = requests.get(f'{url}/get_user/bob')
        assert res.text == '"User_name bob not found"'

    def test_add_get_user(self):
        resp = requests.post(f'{url}/add_user', json={'name': 'Artem'})
        user_id_from_add = resp.json()['user_id']

        resp = requests.get(f'{url}/get_user/Artem')
        user_id_from_get = resp.json()['user_id']

        assert user_id_from_add == user_id_from_get

    def test_add_existent_user(self):
        requests.post(f'{url}/add_user', json={'name': 'Vasya'})
        resp = requests.post(f'{url}/add_user', json={'name': 'Vasya'})

        assert resp.status_code == 400

    def test_get_non_existent_user(self):
        resp = requests.get(f'{url}/Masha')

        assert resp.status_code == 404

    def test_with_age(self):
        requests.post(f'{url}/add_user', json={'name': 'Stepan'})

        resp = requests.get(f'{url}/get_user/Stepan')
        age = resp.json()['age']
        assert isinstance(age, int)
        assert 18 <= age <= 105

    def test_has_surname(self, save_file_surname_root):
        requests.post(f'{url}/add_user', json={'name': 'Olya'})
        surname_data = {'Olya': 'OLOLOEVA'}
        with open(save_file_surname_root, 'w') as file:
            json.dump(surname_data, file)
        resp = requests.get(f'{url}/get_user/Olya')
        surname = resp.json()['surname']
        assert surname == 'OLOLOEVA'

    def test_has_no_surname(self):
        requests.post(f'{url}/add_user', json={'name': 'Sveta'})

        resp = requests.get(f'{url}/get_user/Sveta')
        surname = resp.json()['surname']
        assert surname is None

    def test_update_user_fav_color(self):
        requests.post(f'{url}/add_user', json={'name': 'Monad'})

        resp = requests.put(f'{url}/update_user_fav_color/Monad', json={'color': 'black'})
        color = resp.json()['fav_color']["Monad"]
        assert color == 'black'

    def test_update_user_fav_color_not_valid_color(self):
        requests.post(f'{url}/add_user', json={'name': 'Monad'})

        resp = requests.put(f'{url}/update_user_fav_color/Monad', json={'color': 'smooth'})
        invalid_color_resp = resp.json()
        assert resp.status_code == 400
        assert 'Color smooth not acceptable' in invalid_color_resp

    def test_update_user_fav_color_no_user(self):
        resp = requests.put(f'{url}/update_user_fav_color/Akira', json={'color': 'red'})
        assert resp.status_code == 404
        assert "User_name Akira not found" in resp.json()

    def test_delete_user_age(self):
        requests.post(f'{url}/add_user', json={'name': 'Killy'})

        resp_delete = requests.delete(f'{url}/delete_user_age/Killy')
        assert resp_delete.status_code == 200
        assert "User Killy's age was deleted" in resp_delete.json()

    def test_delete_user_age_no_user(self):
        resp_delete = requests.delete(f'{url}/delete_user_age/Lain')
        assert resp_delete.status_code == 404
        assert "User_name Lain not found" in resp_delete.json()
