import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

        if self.authorize:
            self.api_client.auth()
