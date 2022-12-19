import allure
import pytest
from random import randint

from base import ApiBase
from mysql_client.mysql_client import MysqlClient
from faker import Faker
from utils.builder import Builder

fake = Faker()


@pytest.mark.API_SQL
class TestApiSQL(ApiBase):
    authorize = False

    @pytest.fixture(scope='function', autouse=True)
    def db_mysql(self):
        self.mysql_client = MysqlClient('vkeducation', 'test_qa', 'qa_test')
        self.mysql_client.connect()
        yield self.mysql_client
        self.mysql_client.connection.close()

    @pytest.fixture()
    def sql_inject_and_auth(self):
        new_user = self.new_user
        self.mysql_client.insert_query(
            name=new_user.fake_name,
            surname=new_user.fake_surname,
            middle_name=new_user.fake_middle_name,
            username=new_user.fake_username,
            password=new_user.fake_password,
            email=new_user.fake_email
        )
        auth = self.api_client.auth()
        return new_user, auth

    def sql_inject_and_auth_credentials(self, username=None, password=None):
        new_user = self.new_user
        self.mysql_client.insert_query(
            name=new_user.fake_name,
            surname=new_user.fake_surname,
            middle_name=new_user.fake_middle_name,
            username=new_user.fake_username,
            password=new_user.fake_password,
            email=new_user.fake_email
        )
        if password is None:
            auth = self.api_client.auth_special_creds(username=username, password=new_user.fake_password)
        elif username is None:
            auth = self.api_client.auth_special_creds(username=new_user.fake_username, password=password)
        elif username is not None and password is not None:
            auth = self.api_client.auth_special_creds(username=username, password=password)
        return new_user, auth

    @allure.step("Testing API app status.")
    def test_app_status(self):
        """
        Тестирование статуса приложения.
        Отправляется запрос на ручку /status. Ожидаемый результат - status_code == 200.
        """
        status = self.api_client.check_app_status()
        assert status.status_code == 200

    @allure.step("Testing API authorization works.")
    def test_auth(self, sql_inject_and_auth):
        """
        Тестирование логина через отправление запроса.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Ожидаемый результат - статус код 200. А так же проводится проверка того, что юзер действительно
        записался в базу. Ожидаемый результат - username в респонсе sql на селект данного юзера.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        assert auth.status_code == 200
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert new_user.fake_username in sql_resp[0].items()[4][1]

    @allure.step("Testing API authorization with invalid username.")
    @pytest.mark.parametrize('username', ['invalid', 'привет', '@@@@', '1', '``', '????', '****'])
    def test_auth_invalid_username(self, username):
        """
        Параметризованное тестирование авторизации под невалидным юзернеймом.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его невалидным юзернеймом
        из параметров и валидным паролем. Ожидаемы результат - статус код ответа 401. А так же проводится проверка
        того, что юзер действительно записался в базу. Ожидаемый результат - username в респонсе sql на селект
        данного юзера.
        :param username:
        """
        new_user, auth = self.sql_inject_and_auth_credentials(username=username)
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert new_user.fake_username in sql_resp[0].items()[4][1]
        assert auth.status_code == 401, "Bug with invalid status code returning from server."

    @allure.step("Testing API authorization with invalid password.")
    @pytest.mark.parametrize('password', ['invalid', 'привет', '@@@@', '1', '``', '????'])
    def test_auth_invalid_password(self, password):
        """
        Параметризованное тестирование авторизации с невалидным паролем.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его невалидным юзернеймом
        из параметров и валидным паролем. Ожидаемы результат - статус код ответа 401. А так же проводится проверка
        того, что юзер действительно записался в базу. Ожидаемый результат - username в респонсе sql на селект
        данного юзера.
        :param password:
        """
        new_user, auth = self.sql_inject_and_auth_credentials(password=password)
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert new_user.fake_username in sql_resp[0].items()[4][1]
        assert auth.status_code == 401

    @allure.step("Testing API user deletion works.")
    def test_delete(self, sql_inject_and_auth):
        """
        Тестирование удаления юзера.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется API запрос на удаление пользователя. Ожидаемый результат - статус код 204.
        А так же проводится проверка того, что юзер был удален из базы. Ожидаемый результат - пустой лист ответа sql бд.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        delete = self.api_client.delete_user()
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp == []
        assert delete.status_code == 204

    @allure.step("Testing API user deletion from the session of other user.")
    def test_delete_other_user(self, sql_inject_and_auth):
        """
        Тестирование удаления юзера из сессии другого.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее создается еще один пользователь, отправляется API запрос на удаление 2 пользователя из сессии первого.
        Ожидаемый результат - пользователь не удален, статус код ответа не равен 204.
        :param sql_inject_and_auth:
        """
        builder = Builder()
        new_user_for_del = builder.app_user()
        self.mysql_client.insert_query(
            name=new_user_for_del.fake_name,
            surname=new_user_for_del.fake_surname,
            middle_name=new_user_for_del.fake_middle_name,
            username=new_user_for_del.fake_username,
            password=new_user_for_del.fake_password,
            email=new_user_for_del.fake_email
        )
        delete = self.api_client.delete_other_user(new_user_for_del.fake_username)
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_del.fake_username}";', fetch=True)
        assert sql_resp != [], "Bug. It is possible to delete other users from user session."
        assert delete.status_code != 204

    @allure.step("Testing API user deletion without authorization.")
    def test_delete_unauthorized(self):
        """
        Тестирование удаления юзера.
        Создается новый юзер и записывается напрямую в базу.
        Далее отправляется API запрос на удаление пользователя. Ожидаемый результат - статус код 401.
        А так же проводится проверка того, что юзер не был удален из базы.
        Ожидаемый результат - юзер присутствует в базе.
        """
        builder = Builder()
        new_user_for_del = builder.app_user()
        self.mysql_client.insert_query(
            name=new_user_for_del.fake_name,
            surname=new_user_for_del.fake_surname,
            middle_name=new_user_for_del.fake_middle_name,
            username=new_user_for_del.fake_username,
            password=new_user_for_del.fake_password,
            email=new_user_for_del.fake_email
        )
        delete = self.api_client.delete_other_user(new_user_for_del.fake_username)
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_del.fake_username}";', fetch=True)
        assert sql_resp[0][4] == new_user_for_del.fake_username
        assert delete.status_code == 401

    @allure.step("Testing API user password updating works.")
    def test_update_password(self, sql_inject_and_auth):
        """
        Тестирование обновления пароля пользователя.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется запрос на обновление пароля. Ожидаемый результат - статус код 204. Так же проверяются
        записи в бд, а именно: пользователь существует в базе, пароль пользователся не совпадает с первоначальным
        паролем, который был у пользователя при регистрации, и что пароль в бд - это обновленыый пароль.
        :param sql_inject_and_auth:
        """
        new_pass = 'vkeducation_pass'
        new_user, auth = sql_inject_and_auth
        upd = self.api_client.update_user_password(new_pass=new_pass)
        assert upd.status_code == 204
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][4] == new_user.fake_username
        assert sql_resp[0][5] != new_user.fake_password
        assert sql_resp[0][5] == new_pass

    @allure.step("Testing API user password updating with the same password.")
    def test_update_password_matches_recent(self, sql_inject_and_auth):
        """
        Тестирование обновления пароля пользователя паролем, который уже есть.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется запрос на обновление пароля со значением предыдущего. Ожидаемый результат -
        статус код не равен 204. Так же проверяются записи в бд, а именно: пользователь существует в базе,
        пароль пользователя совпадает с первоначальным паролем, который был у пользователя при регистрации.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        upd = self.api_client.update_user_password(new_pass=new_user.fake_password)
        assert upd.status_code != 204, "Bug. It is possible to update password with the same value."
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][4] == new_user.fake_username
        assert sql_resp[0][5] == new_user.fake_password

    @allure.step("Testing API user password updating with empty value")
    def test_update_password_no_value(self, sql_inject_and_auth):
        """
        Тестирование обновления пароля пользователя пустым паролем.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется запрос на обновление пароля с пустым значением. Ожидаемый результат -
        статус код не равен 204. Так же проверяются записи в бд, а именно: пользователь существует в базе,
        пароль пользователя не пуст.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        upd = self.api_client.update_user_password(new_pass='')
        assert upd.status_code != 204, "Bug. It is possible to update password with empty value."
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][4] == new_user.fake_username
        assert sql_resp[0][5] != ''

    @allure.step("Testing API user password updating with value None.")
    def test_update_password_none(self, sql_inject_and_auth):
        """
        Тестирование обновления пароля пользователя паролем None.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется запрос на обновление пароля со значением None. Ожидаемый результат -
        статус код 304 или 400. Так же проверяются записи в бд, а именно: пользователь существует в базе,
        пароль пользователя не пуст.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        upd = self.api_client.update_user_password(new_pass=None)
        assert upd.status_code == 304 or upd.status_code == 400,\
            "Bug. Changing password with None value crashes server."
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][4] == new_user.fake_username
        assert sql_resp[0][5] == new_user.fake_password

    @allure.step("Testing API user password updating from other users session.")
    def test_update_password_other_user(self, sql_inject_and_auth):
        """
        Тестирование обновления пароля одного пользователя из сессии другого.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется запрос на обновление пароля другого юзера со значением. Ожидаемый результат -
        статус код не равен 204. Так же проверяются записи в бд, а именно: пользователь существует в базе,
        пароль пользователя не равен паролю, на который производилась попытка обновления.
        :param sql_inject_and_auth:
        """
        user_to_be_updated = 'captain'
        new_password = randint(100, 1000)
        upd = self.api_client.update_other_user_password(new_pass=new_password, username=user_to_be_updated)
        assert upd.status_code != 204, "Bug. It is possible to update password of other user."
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{user_to_be_updated}";', fetch=True)
        assert sql_resp[0][4] == user_to_be_updated
        assert sql_resp[0][5] != new_password

    @allure.step("Testing API user block works.")
    def test_block_user(self, sql_inject_and_auth):
        """
        Тестирование блокировки пользователя.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        Далее отправляется запрос на API блокировки. Ожидаемый результат - статус код 200.
        Так же проверятся запись в бд, а именно, что access у выбранного пользователя - 0.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        block = self.api_client.block_user()
        assert block.status_code == 200
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][7] == 0

    @allure.step("Testing API user unblock works.")
    def test_unblock_user(self, sql_inject_and_auth):
        """
        Тестирование разблокировки пользователя.
        Тест создает нового юзера напрямую в базе данных и авторизуется под ним, после чего дергает апи ручку
        блокировки. После этого дергается ручка разблокировки. Ожидаемый результат - разблокировка успешна.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        block = self.api_client.block_user()
        assert block.status_code == 200
        unblock = self.api_client.unblock_user()
        assert unblock.status_code == 200, "Bug with unblocking a user. Only possible from the session of another user."
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][7] == 1

    @allure.step("Testing API user unblock works.")
    def test_unblock_user_other_session(self, sql_inject_and_auth):
        """
        Тестирование разблокировки из-под сессии другого пользователя.
        Тест создает нового юзера напрямую в базе данных и авторизуется под ним, после чего дергает апи ручку
        блокировки. После этого создается еще один юзер в бд, происходит авторизация под ним, после чего отправляется
        запрос на разблокировку первого пользователя из сессии второго. Ожидаемый результат - статус код 401.
        :param sql_inject_and_auth:
        """
        new_user, auth = sql_inject_and_auth
        block = self.api_client.block_user()
        assert block.status_code == 200
        builder = Builder()
        new_user_who_unblocks = builder.app_user()
        self.mysql_client.insert_query(
            name=new_user_who_unblocks.fake_name,
            surname=new_user_who_unblocks.fake_surname,
            middle_name=new_user_who_unblocks.fake_middle_name,
            username=new_user_who_unblocks.fake_username,
            password=new_user_who_unblocks.fake_password,
            email=new_user_who_unblocks.fake_email
        )
        self.api_client.auth_special_creds(username=new_user_who_unblocks.fake_username,
                                           password=new_user_who_unblocks.fake_password)
        unblock = self.api_client.unblock_user_other_session(username_to_unblock=new_user.fake_username)
        assert unblock.status_code == 401, "Bug with unblocking a user. Only possible from the session of another user."
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][7] == 0

    @allure.step("Testing API registration as it should work according to docs.")
    def test_reg_normal(self):
        """
        Тестирование регистрации через API.
        Производится генерация нового юзера, после чего происходит попытка регистрации через API ручку.
        Ожидаемый результат - регистрация успешна, статус код 201. Так же производится проверка бд на предмет
        того, что юзер действительно записан.
        """
        new_user = self.new_user
        reg = self.api_client.register_new_user(new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name,
                                                new_user.fake_username, new_user.fake_password, new_user.fake_email)
        assert reg.status_code == 201, 'Bug with registration via API. Only possible under the session of other user.'
        assert reg.text == '{"detail":"User was added","status":"success"}\n'
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user.fake_username}";', fetch=True)
        assert sql_resp[0][4] == new_user.fake_username

    @allure.step("Testing API registration with injection of a cookie of a registered user.")
    def test_reg_cookie_injection(self, sql_inject_and_auth):
        """
        Тестирование регистрации через API под сессией зарегистрированного юзера.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        После производится генерация 2 нового юзера, после чего происходит попытка регистрации через API ручку под
        сессией 1 нового юзера. Ожидаемый результат - регистрация не успешна, текст ответа не содержит сообщение
        об успешной регистрации и статус код не равен 201. Так же производится проверка бд на предмет
        того, что юзера нет в бд.
        :param sql_inject_and_auth:
        """
        builder = Builder()
        new_user_for_reg = builder.app_user()
        reg = self.api_client.register_new_user_cookie_inject(
            new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
            new_user_for_reg.fake_username, new_user_for_reg.fake_password, new_user_for_reg.fake_email)
        assert reg.text != '{"detail":"User was added","status":"success"}\n',\
            'Bug with registration via API. Only possible under the session of other user.'
        assert reg.status_code != 201
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_reg.fake_username}";', fetch=True)
        assert sql_resp == []

# Дальнейшие тесты используют регистрацию с использованием сессии юзера, считающуюся неправильным поведением.

    @allure.step("Testing API registration with injection of a cookie of a registered user.")
    @pytest.mark.parametrize('username', ['', '      ', '1', 'a', 'алло', '@@@@', 'ttttttttttttttttt'])
    def test_reg_cookie_injection_invalid_username(self, sql_inject_and_auth, username):
        """
        Параметризованное тестирование регистрации через API под сессией зарегистрированного юзера.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        После производится генерация 2 нового юзера, после чего происходит попытка регистрации через API ручку под
        сессией 1 нового юзера с невалидным username. Ожидаемый результат - регистрация не успешна,
        текст ответа не содержит сообщение об успешной регистрации и статус код не равен 201 и 500.
        Так же производится проверка бд на предмет того, что юзера нет в бд.
        :param sql_inject_and_auth:
        :param username:
        """
        builder = Builder()
        new_user_for_reg = builder.app_user()
        reg = self.api_client.register_new_user_cookie_inject(
            new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
            username, new_user_for_reg.fake_password, new_user_for_reg.fake_email)
        assert reg.text != '{"detail":"User was added","status":"success"}\n', \
            'Bug. Possible to register with invalid username.'
        assert reg.status_code != 201
        assert reg.status_code != 500, 'Bug. Registration with username longer than 16 chars returns 500 status code.'
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_reg.fake_username}";', fetch=True)
        assert sql_resp == []

    @allure.step("Testing API registration with injection of a cookie of a registered user.")
    @pytest.mark.parametrize('password', ['', '  ', '   ', '    ', '      ', '1 2 3 4 5'])
    def test_reg_cookie_injection_invalid_password(self, sql_inject_and_auth, password):
        """
        Параметризованное тестирование регистрации через API под сессией зарегистрированного юзера.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        После производится генерация 2 нового юзера, после чего происходит попытка регистрации через API ручку под
        сессией 1 нового юзера с невалидным паролем. Ожидаемый результат - регистрация не успешна,
        текст ответа не содержит сообщение об успешной регистрации и статус код не равен 201.
        Так же производится проверка бд на предмет того, что юзера нет в бд.
        :param sql_inject_and_auth:
        :param password:
        """
        builder = Builder()
        new_user_for_reg = builder.app_user()
        reg = self.api_client.register_new_user_cookie_inject(
            new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
            new_user_for_reg.fake_username, password, new_user_for_reg.fake_email)
        assert reg.text != '{"detail":"User was added","status":"success"}\n', \
            'Bug. Possible to register with invalid password.'
        assert reg.status_code != 201
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_reg.fake_username}";', fetch=True)
        assert sql_resp == []

    @allure.step("Testing API registration with injection of a cookie of a registered user.")
    @pytest.mark.parametrize('email', ['', '  ', '1 2 3 4 5', 'no_email', '@'])
    def test_reg_cookie_injection_invalid_email(self, sql_inject_and_auth, email):
        """
        Параметризованное тестирование регистрации через API под сессией зарегистрированного юзера.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        После производится генерация 2 нового юзера, после чего происходит попытка регистрации через API ручку под
        сессией 1 нового юзера с невалидным email. Ожидаемый результат - регистрация не успешна,
        текст ответа не содержит сообщение об успешной регистрации и статус код не равен 201.
        Так же производится проверка бд на предмет того, что юзера нет в бд.
        :param sql_inject_and_auth:
        :param email:
        """
        builder = Builder()
        new_user_for_reg = builder.app_user()
        reg = self.api_client.register_new_user_cookie_inject(
            new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
            new_user_for_reg.fake_username, new_user_for_reg.fake_password, email)
        assert reg.text != '{"detail":"User was added","status":"success"}\n', \
            'Bug. Possible to register with invalid email.'
        assert reg.status_code != 201
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_reg.fake_username}";', fetch=True)
        assert sql_resp == []

    @allure.step("Testing API registration with injection of a cookie of a registered user.")
    @pytest.mark.parametrize('field', ['name', 'surname', 'username', 'password', 'email'])
    def test_reg_cookie_injection_no_req_fields(self, sql_inject_and_auth, field):
        """
        Параметризованное тестирование регистрации через API под сессией зарегистрированного юзера со значениями None.
        Создается новый юзер и записывается напрямую в базу. После производится логин под его кредами.
        После производится генерация 2 нового юзера, после чего происходит попытка регистрации через API ручку под
        сессией 1 нового юзера с одним из обязательных полей со значением None.
        Ожидаемый результат - регистрация не успешна, текст ответа не содержит сообщение об успешной регистрации
        и статус код не равен 500. Так же производится проверка бд на предмет того, что юзера нет в бд.
        :param sql_inject_and_auth:
        :param field:
        """
        builder = Builder()
        new_user_for_reg = builder.app_user()
        if field == 'name':
            reg = self.api_client.register_new_user_cookie_inject(
                None, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
                new_user_for_reg.fake_username, new_user_for_reg.fake_password, new_user_for_reg.fake_email)
        elif field == 'surname':
            reg = self.api_client.register_new_user_cookie_inject(
                new_user_for_reg.fake_name, None, new_user_for_reg.fake_middle_name,
                new_user_for_reg.fake_username, new_user_for_reg.fake_password, new_user_for_reg.fake_email)
        elif field == 'username':
            reg = self.api_client.register_new_user_cookie_inject(
                new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
                None, new_user_for_reg.fake_password, new_user_for_reg.fake_email)
        elif field == 'password':
            reg = self.api_client.register_new_user_cookie_inject(
                new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
                new_user_for_reg.fake_username, None, new_user_for_reg.fake_email)
        elif field == 'email':
            reg = self.api_client.register_new_user_cookie_inject(
                new_user_for_reg.fake_name, new_user_for_reg.fake_surname, new_user_for_reg.fake_middle_name,
                new_user_for_reg.fake_username, new_user_for_reg.fake_password, None)
        assert reg.status_code != 500,\
            'Bug. Registration with None required values causes server error or lets register with NULL value.'
        assert reg.text != '{"detail":"User was added","status":"success"}\n'
        sql_resp = self.mysql_client.execute_query(
            f'SELECT * FROM test_users WHERE username="{new_user_for_reg.fake_username}";', fetch=True)
        assert sql_resp == []
