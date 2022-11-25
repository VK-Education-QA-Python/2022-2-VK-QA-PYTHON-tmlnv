import pytest
from my_sql.client import MysqlClient
from utils.builder import MysqlBuilder
from models.tasks import Task1Model, Task2Model, Task3Model, Task4Model, Task5Model
from python_scripts import AnalyzeScript


class Prepare:

    def prepare_tables(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.client: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.client)

    def get_task(self, task_model, **filters):
        self.client.session.commit()
        return self.client.session.query(task_model).filter_by(**filters).all()


@pytest.mark.SQL
class TestMysql(Prepare):
    run_script = AnalyzeScript()

    def test_task1(self):
        self.builder.insert_task1()
        task1 = self.get_task(Task1Model)
        res1 = self.run_script.solve_task1()
        assert len(task1) == 1
        assert str(res1) in str(task1[0])

    def test_task2(self):
        self.builder.insert_task2()
        task2 = self.get_task(Task2Model)
        res2 = self.run_script.solve_task2()
        assert len(task2) == len(res2)
        assert str(res2["GET"]) in str(task2[0])

    def test_task3(self):
        self.builder.insert_task3()
        task3 = self.get_task(Task3Model)
        res3 = self.run_script.solve_task3(number_of_most_to_display=10)
        assert len(task3) == len(res3)
        assert str(res3['/administrator/index.php']) in str(task3[0])

    def test_task4(self):
        self.builder.insert_task4()
        task4 = self.get_task(Task4Model)
        res4 = self.run_script.solve_task4(number_of_most_to_display=5)
        assert len(task4) == len(res4)
        first_ip = ''
        for i in res4.keys():
            first_ip = i[0]
            break
        assert first_ip in str(task4[0])

    def test_task5(self):
        self.builder.insert_task5()
        task5 = self.get_task(Task5Model)
        res5 = self.run_script.solve_task5(number_of_most_to_display=5)
        assert len(task5) == len(res5)
        assert str(res5['189.217.45.73']) in str(task5[0])
