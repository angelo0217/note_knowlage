#[壓力測試](https://hackmd.io/@-jz62VB3TX-Bd4LAU5urGg/BkltPSg0t)
# Python
## install
```shell
安裝 python windows 版

power shell 執行，安裝poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

env
PYTHON_HOME: D:\tool\python3.9.10
path添加
  %PYTHON_HOME%
  poetry 位置，已安裝時提供為主
  C:\Users\g02117\AppData\Roaming\Python\Scripts
```

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
## partition split
```python
partition_list = [object_list[i : i + 10000] for i in range(0, len(object_list), 10000)]
```
## mocked sample 
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
    mocked_session.return_value.resource.return_value.Table.return_value.get_item.side_effect = RuntimeError(
        "test")
```
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


@patch.object(XXXXClass, "cccFunc")
def test_post_coverages_400(
    mocked_func
):
    mocked_func.return_value = 85
    req_body = mocked_create_coverage_body
    .....
```
```python
@pytest.mark.parametrize(
    "http_code",
    [
        (HTTPStatus.BAD_REQUEST),
        (HTTPStatus.OK),
    ],
)
```
```python
@pytest.fixture
def mocked_send_message():
    session = MagicMock()
    with patch.object(xxxx.ccc.sss, "Session", return_value=session):
        client = session.client()
        yield client.send_message

        
@pytest.fixture
def mocked_some_function():
    with patch.object(
        aaa.bbb.ccc,
        "xx_funct",
    ) as some_function:
        some_function.return_value = "test.com"
        yield some_function


def test_xxxx(mocked_send_message, mocked_some_function, session):
    mocked_send_message.assert_called()
```
```python
with pytest.raises(Exception):
    xxxx()
```
# pytest class
```python
@pytest.mark.usefixtures("xxxx")
class TestSomeClass:

    @patch("xxx.xxx.aaa")
    def test_response_200(
        self, mocked_aaa
    ):
        mocked_aaa.return_value = tms_truck_information
        do_some_thing()
```
# python cdc
```python
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)


# mysql-replication = "*" 安裝此包
#  env add PYTHONUTF8=1  windows 環境變數須加上這個

def main():

    MYSQL_SETTINGS = {
        "host": "127.0.0.1",
        "port": 3307,
        "user": "root",
        "passwd": "Java1234!"
    }
    '''
    * server_id is your slave identifier, it should be unique.
    * set blocking to True if you want to block and wait for the next event at
    the end of the stream
    * only_events will listen only to describes events 
    '''
    print(">>>listener start streaming to:mysql_data")

    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=2,
        blocking=True,
        resume_stream=True,
        filter_non_implemented_events=False,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
        only_tables=["books"],
        log_file="mysql-bin.000013", # 若無file設定，則只會撈最新，有則從對應file後面都撈
        log_pos=4,
    )

    for binlogevent in stream:
        print("当前的 log_file 名称为:", stream.log_file)
        print(">>>binlogevent: ", binlogevent.to_dict())
        for row in binlogevent.rows:
            print(">>> start event")
            event = {"schema": binlogevent.schema,
                     "table": binlogevent.table,
                     "type": type(binlogevent).__name__,
                     "row": row
                     }
            print(">>>event", event)

            # binlogevent.dump()

    stream.close()


if __name__ == "__main__":
    main()

```