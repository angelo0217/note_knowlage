docker-compose
添加binlog的應用
```shell my.cnf 
[mysqld]
log-bin=mysql-bin
binlog_format=ROW
secure_file_priv=""
server_id=1
binlog_row_metadata=FULL
binlog_row_image=FULL
```
```yaml
version: '3.7'
services:
  demo-mysql:
    image: mysql:8.0.25
    container_name: mysql
    command: mysqld --default-authentication-plugin=mysql_native_password --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --wait_timeout=10 --interactive_timeout=10
    ports:
      - '3306:3306'
    environment:
      MYSQL_ROOT_PASSWORD: Java1234!
      MYSQL_DATABASE: mydb
    volumes:
      - ./my.cnf:/etc/mysql/my.cnf
      - mysql_data:/var/lib/mysql
volumes:
  mysql_data:
```
```sql
CREATE DATABASE test_db;
```
```sql
CREATE TABLE `test_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX idx_job_name ON test_table(jenkins_job);
```
```sql
CREATE USER 'test'@'%' IDENTIFIED BY 'testpwd';
GRANT ALL PRIVILEGES ON test_db.* TO 'test'@'%';
GRANT ALL PRIVILEGES ON mydb.* TO 'test'@'%';

ALTER USER  'test'@'%' IDENTIFIED BY '!QAZ2wsx';
```
```sql
CREATE VIEW deploy_view AS
    select package_name, package_version from mop_deploy_package;
create or replace view deploy_view as
       select package_name, package_version from mop_deploy_package;
create or replace view deploy_view2 as
    select v.id, v.git_project, p.package_name, p.package_version from test_db.mop_deploy_version v
    left join mop_deploy_package p on p.deploy_id = v.id 
SHOW TABLE STATUS LIKE 'user_view';
```
# [參考](https://dev.mysql.com/doc/refman/5.7/en/create-user.html)
python read binlog
WINDOWS 環境變數先加上 PYTHONUTF8=1
安裝 mysql-replication   poetry add mysql-replication
```python

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

def main():

    MYSQL_SETTINGS = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "Java1234!"
    }
    print(">>>listener start streaming to:mysql_data")
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=1,
        blocking=True,
        resume_stream=True,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
        only_tables=["books"]
    )
    for binlogevent in stream:
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
