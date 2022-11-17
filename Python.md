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
## local queue
```python
from queue import PriorityQueue


class PriorityQueueWithKey(PriorityQueue):
    def __init__(self, key=None, maxsize=0):
        super().__init__(maxsize)
        self.key = key

    def put(self, item):
        if self.key is None:
            super().put((item, item))
        else:
            super().put((self.key(item), item))

    def get(self):
        return super().get(self.queue)[1]


class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New Job', description)
        return
    def __lt__(self, other):
        return self.priority > other.priorit

if __name__ == '__main__':
    a = PriorityQueueWithKey(abs)
    a.put(-4)
    a.put(-3)
    print(*a.queue)

    print(a.get())

    print(*a.queue)

    q2 = PriorityQueue();
    q2.put(Job(5, 'ddd'))
    q2.put(Job(10, 'ccc'))
    q2.put(Job(1, 'aaa'))

    while not q2.empty():
        nextJob = q2.get()
        print('get job:', nextJob.priority)

```
## mocked
```python
from unittest.mock import patch, MagicMock
import boto3

mocked_session = MagicMock()
# boto3 need to project path
with patch.object(
        boto3, "Session", return_value=mocked_session
    ) as mocked_session:
    mocked_session.return_value.resource.return_value.Table.return_value.get_item.return_value = {
            "Item": None
        }

with patch.object(
        boto3, "Session", side_effect=RuntimeError("test")
    ) as mocked_session:
    mocked_session.return_value.resource.return_value.Table.return_value.get_item.side_effect=RuntimeError("test")
```
## sample2
```python
from unittest.mock import patch
from http import HTTPStatus

@patch("xxxx.yyy.zzz.ClassName")
def test_error(
    mocked_class,
    client,
    headers,
):
    mocked_class.return_value.publish.side_effect = RuntimeError("xxx")
    # mocked_class.return_value.publish.side_effect = function_name
    url = "/xxxx/xxxx"
    resp = client.post(url, headers=headers, json={})

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
```