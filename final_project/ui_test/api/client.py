import requests
import allure


class ApiClientException(Exception):
    ...


class ApiClient:

    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url

        self.login = login
        self.password = password

        self.session = requests.Session()

        self.headers = {}

    @allure.step("Authorizing as a registered user.")
    def auth(self):
        headers = {
            'Origin': "http://0.0.0.0:7777",
            'Referer': "http://0.0.0.0:7777/login",
            "Content-Type": "application/x-www-form-urlencoded"

        }
        data = {
            'username': self.login,
            'password': self.password,
            'submit': 'Login',
        }
        auth = self.session.post(url=self.base_url, headers=headers, data=data)
        return auth

    @allure.step("Blocking user.")
    def block_user(self):
        blocked = self.session.post(url='http://0.0.0.0:7777/api/user/' + f'{self.login}' + '/block')
        return blocked
