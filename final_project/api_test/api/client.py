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
        auth = self.session.post(url='http://0.0.0.0:7777/login', headers=headers, data=data)
        return auth

    @allure.step("Authorizing as a registered user.")
    def auth_special_creds(self, username, password):
        headers = {
            'Origin': "http://0.0.0.0:7777",
            'Referer': "http://0.0.0.0:7777/login",
            "Content-Type": "application/x-www-form-urlencoded"

        }
        data = {
            'username': username,
            'password': password,
            'submit': 'Login',
        }
        auth = self.session.post(url='http://0.0.0.0:7777/login', headers=headers, data=data)
        return auth

    @allure.step("Deleting registered user.")
    def delete_user(self):
        deleted = self.session.delete(url='http://0.0.0.0:7777/api/user/' + f'{self.login}')
        return deleted

    @allure.step("Deleting registered user from the session of other user.")
    def delete_other_user(self, username):
        deleted = self.session.delete(url='http://0.0.0.0:7777/api/user/' + f'{username}')
        return deleted

    @allure.step("Updating user password.")
    def update_user_password(self, new_pass):
        headers = {"Content-Type": "application/json"}
        data = {"password": new_pass}
        updated_pass = self.session.put(url='http://0.0.0.0:7777/api/user/' + f'{self.login}' + '/change-password',
                                        headers=headers, json=data)
        return updated_pass

    @allure.step("Updating user password from the session of other user.")
    def update_other_user_password(self, new_pass, username):
        headers = {"Content-Type": "application/json"}
        data = {"password": new_pass}
        updated_pass = self.session.put(url='http://0.0.0.0:7777/api/user/' + f'{username}' + '/change-password',
                                        headers=headers, json=data)
        return updated_pass

    @allure.step("Blocking user.")
    def block_user(self):
        blocked = self.session.post(url='http://0.0.0.0:7777/api/user/' + f'{self.login}' + '/block')
        return blocked

    @allure.step("Unblocking user.")
    def unblock_user(self):
        unblocked = self.session.post(url='http://0.0.0.0:7777/api/user/' + f'{self.login}' + '/accept')
        return unblocked

    @allure.step("Unblocking user uder the session of other user.")
    def unblock_user_other_session(self, username_to_unblock):
        unblocked = self.session.post(url='http://0.0.0.0:7777/api/user/' + f'{username_to_unblock}' + '/accept')
        return unblocked

    @allure.step("Checking app status.")
    def check_app_status(self):
        return self.session.get(url='http://0.0.0.0:7777/status')

    @allure.step("Registering a new user via API.")
    def register_new_user(self, name, surname, middle_name, username, password, email):
        headers = {"Content-Type": "application/json"}
        data = {
            "name": name,
            "surname": surname,
            "middle_name": middle_name,
            "username": username,
            "password": password,
            "email": email
        }
        registered = self.session.post(url='http://0.0.0.0:7777/api/user', headers=headers, json=data)
        return registered

    @allure.step("Registering a new user via API with injection of a cookie of other already registered user.")
    def register_new_user_cookie_inject(self, name, surname, middle_name, username, password, email):
        headers = {"Content-Type": "application/json"}
        data = {
            "name": name,
            "surname": surname,
            "middle_name": middle_name,
            "username": username,
            "password": password,
            "email": email
        }
        registered = self.session.post(url='http://0.0.0.0:7777/api/user', headers=headers, json=data)
        return registered
