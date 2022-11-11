import pytest
from my_sql.client import MysqlClient


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='0000', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_table_task1()
        mysql_client.create_table_task2()
        mysql_client.create_table_task3()
        mysql_client.create_table_task4()
        mysql_client.create_table_task5()

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.delete_db()
    client.connection.close()
