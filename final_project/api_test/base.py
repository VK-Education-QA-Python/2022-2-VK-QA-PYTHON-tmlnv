import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, new_user):
        self.api_client = api_client
        self.new_user = new_user

        if self.authorize:
            self.api_client.auth()
