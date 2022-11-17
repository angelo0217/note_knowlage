# Python
## List Partition
```python
sample_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
n = 3
p_list = [sample_list[i:i + n] for i in range(0, len(sample_list), n)]
```
## current thread
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os, time


def task(n):
    print('%s is runing进程号' % os.getpid())
    time.sleep(1)
    return n ** 2


def main():
    start_time = time.time()
    executor = ThreadPoolExecutor(max_workers=3)
    futures = []
    for i in range(10):
        future = executor.submit(task, i)  # 这里使用submit提交进程
        futures.append(future)
    executor.shutdown(True)
    print('*' * 20)
    for future in futures:
        print(future.result())
    print('用时共： %s second' % (time.time() - start_time))


def main2():
    start_time = time.time()
    executor = ThreadPoolExecutor(max_workers=3)
    future = executor.submit(task, 1)  # 这里使用submit提交进程
    # executor.shutdown(True)
    print('*' * 20)
    print(future.result(timeout=1))
    print('用时共： %s second' % (time.time() - start_time))
```