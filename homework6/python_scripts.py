import os
import re
from collections import Counter
import heapq
from collections import defaultdict
from operator import itemgetter


class AnalyzeScript:
    FILE_PATH_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), './access.log'))

    with open(FILE_PATH_LOG, 'r') as file:
        data = file.readlines()

    def solve_task1(self):
        task1 = len(self.data)
        return task1

    def solve_task2(self):
        DATA = dict()
        i = 0
        for line in self.data:
            i += 1
            DATA[f'method{i}'] = line.split()[5]

        count = Counter(DATA.values())
        task2 = {
            "GET": count['"GET'],
            "POST": count['"POST'],
            "HEAD": count['"HEAD'],
            "PUT": count['"PUT'],
            "IRRELEVANT": count['"g369g=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2bfCIpOztlY2hvKCJlNTBiNWYyYjRmNjc1NGFmMDljYzg0NWI4YjU4ZTA3NiIpOztlY2hvKCJ8PC0iKTs7ZGllKCk7GET']
        }
        return task2

    def solve_task3(self, number_of_most_to_display):
        with open(self.FILE_PATH_LOG, "r") as f:
            counter = Counter(''.join(line.split()[6]) for line in f)

        task3 = dict()
        for url, count in counter.most_common(number_of_most_to_display):
            task3[url] = count
        return task3

    def solve_task4(self, number_of_most_to_display):
        access = defaultdict()
        with open(self.FILE_PATH_LOG, "r") as f:
            for line in f:
                parts = line.split()
                if re.search('4[0-9][0-9]', parts[8]):
                    access[line] = parts[9]

        task4 = dict()
        k = number_of_most_to_display
        for line, part in heapq.nlargest(k, access.items(), key=itemgetter(1)):
            task4[(line.split()[0], line.split()[6], line.split()[8])] = part
        return task4

    def solve_task5(self, number_of_most_to_display):
        access = defaultdict(int)
        with open(self.FILE_PATH_LOG, "r") as f:
            for line in f:
                parts = line.split()
                if re.search('5[0-9][0-9]', parts[8]):
                    access[parts[0]] += 1

        task5 = dict()
        k = number_of_most_to_display
        for ip, count in heapq.nlargest(k, access.items(), key=itemgetter(1)):
            task5[ip] = count
        return task5
