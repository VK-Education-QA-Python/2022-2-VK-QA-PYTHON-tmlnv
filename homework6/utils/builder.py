from models.tasks import Task1Model, Task2Model, Task3Model, Task4Model, Task5Model
from python_scripts import AnalyzeScript


class MysqlBuilder:

    analyze = AnalyzeScript()
    res1 = analyze.solve_task1()
    res2 = analyze.solve_task2()
    res3 = analyze.solve_task3()
    res4 = analyze.solve_task4()
    res5 = analyze.solve_task5()

    def __init__(self, client):
        self.client = client

    def insert_task1(self):
        self.client.session.add(
            Task1Model(total_number_of_requests=f'{self.res1}')
        )

    def insert_task2(self):
        methods = []
        vals = []
        for k, v in self.res2.items():
            methods.append(k)
            vals.append(v)
        for i in range(len(methods)):
            arg = Task2Model(method=f'{methods[i]}', number_of_requests=vals[i])
            self.client.session.add(arg)

    def insert_task3(self):
        urls = []
        vals = []
        for k, v in self.res3.items():
            urls.append(k)
            vals.append(v)
        for i in range(len(urls)):
            arg = Task3Model(url=f'{urls[i]}', number_of_requests=vals[i])
            self.client.session.add(arg)

    def insert_task4(self):
        data = []
        vals = []
        for k, v in self.res4.items():
            data.append(k)
            vals.append(v)
        for i in range(len(data)):
            arg = Task4Model(ip=f'{data[i][0]}', url=f'{data[i][1]}', status_code=f'{data[i][2]}',
                             request_size=int(vals[i]))
            self.client.session.add(arg)

    def insert_task5(self):
        ips = []
        vals = []
        for k, v in self.res5.items():
            ips.append(k)
            vals.append(v)
        for i in range(len(ips)):
            arg = Task5Model(ip=f'{ips[i]}', number_of_requests=vals[i])
            self.client.session.add(arg)

    # def prepare_tables(self):
    #     self.create_task1()
    #     self.create_task2()
    #     self.create_task3()
    #     self.create_task4()
    #     self.create_task5()
