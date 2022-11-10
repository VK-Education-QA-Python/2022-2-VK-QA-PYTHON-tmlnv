import argparse
import re
from collections import Counter
import json
import heapq
from collections import defaultdict
from operator import itemgetter


parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
jsonify = parser.parse_args()

with open('access.log', 'r') as file:
    data = file.readlines()

# 1
print("*" * 40)
print("TASK 1")
task1 = len(data)
print("Total number of requests", len(data))
print("*" * 40)

# 2
print("*" * 40)
print("TASK 2")
DATA = dict()
i = 0
for line in data:
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
print(task2)

# 3
print("*" * 40)
print("TASK 3")
with open("access.log", "r") as f:
    counter = Counter(''.join(line.split()[6]) for line in f)

task3 = dict()
for url, count in counter.most_common(10):
    print(f"{url} {count}")
    task3[url] = count
print("*" * 40)

# 4
print("*" * 40)
print("TASK 4")
access = defaultdict()
with open("access.log", "r") as f:
    for line in f:
        parts = line.split()
        if re.search('4[0-9][0-9]', parts[8]):
            access[line] = parts[9]

task4 = dict()
k = 5
for line, part in heapq.nlargest(k, access.items(), key=itemgetter(1)):
    print(f"{line.split()[0]} {line.split()[6]} {line.split()[8]} {part}")
    task4[f'{line.split()[0]} {line.split()[6]} {line.split()[8]}'] = part
print("*" * 40)

# 5
print("*" * 40)
print("TASK 5")
access = defaultdict(int)
with open("access.log", "r") as f:
    for line in f:
        parts = line.split()
        if re.search('5[0-9][0-9]', parts[8]):
            access[parts[0]] += 1

task5 = dict()
k = 5
for ip, count in heapq.nlargest(k, access.items(), key=itemgetter(1)):
    print(f"{ip} {count}")
    task5[ip] = count
print("*" * 40)

# making result json
if jsonify.json:
    result = {
        'task1 (total requests)': task1,
        'task2 (total requests by method)': task2,
        'task3 (top 10 most frequent requests)': task3,
        'task4 (top 5 largest 4XX requests)': task4,
        'task5 (top 5 users by number of requests that ended 5XX': task5
    }
    json_object = json.dumps(result, indent=5)
    with open('results_python.json', 'w') as result_file:
        result_file.write(json_object)
