#!/bin/bash
echo "task1 (total requests)" > results_bash.txt
cat access.log | wc -l >> results_bash.txt
echo "task2 (total requests by method)" >> results_bash.txt
awk '{a[substr($6,2)]++}END{for(i in a) print i,a[i] | "sort -rnk2"}' access.log >> results_bash.txt
echo "task3 (top 10 most frequent requests)" >> results_bash.txt
cut -d ' ' -f7 access.log | sort | uniq -c | sort -rn | head -n10 >> results_bash.txt
echo "task4 (top 5 largest 4XX requests)" >> results_bash.txt
cut -d ' ' -f7 -f9 -f10 -f1 access.log | grep "\s4[0-9][0-9]\s" | sort -rk4 | head -n5 >> results_bash.txt
echo "task5 (top 5 users by number of requests that ended 5XX)" >> results_bash.txt
cut -d ' ' -f1 -f9 access.log | grep "5[0-9][0-9]" | sort | uniq -c |sort -r | head -n5 | awk '{print $1" " $2}' >> results_bash.txt