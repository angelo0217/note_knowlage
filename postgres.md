#[教學](https://pjchender.dev/database/psql-roles-privilege/)
#[中文手冊](https://docs.postgresql.tw/server-programming/the-rule-system/materialized-views)
#[docker](https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec)
##[docker操作](https://myapollo.com.tw/zh-tw/docker-postgres/)
##docker-compose
```yaml
version: '3.7'
services:
  postgres:
    image: postgres:12.4-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=mudb
      - POSTGRES_PASSWORD=1qaz2wsx
      - PGDATA=/var/lib/postgresql/data/pgdata
    restart: always
```
# sql語法
##[GRANT](https://pjchender.dev/database/psql-roles-privilege/)
```sql
CREATE DATABASE test_db;
CREATE USER dean WITH PASSWORD '1qaz2wsx';
GRANT ALL PRIVILEGES ON DATABASE test_db TO dean;
```

#[Schema](https://www.runoob.com/postgresql/postgresql-schema.html)
```sql
create schema my_schema

CREATE TABLE "my_schema".COMPANY3(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);

GRANT USAGE ON SCHEMA my_schema TO mydb;
GRANT ALL ON ALL TABLES IN SCHEMA my_schema TO mydb;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA schema_a TO dean;
GRANT ALL ON ALL SEQUENCES IN SCHEMA my_schema TO mydb;
```

#[cross db search](https://docs.aiven.io/docs/products/postgresql/howto/use-dblink-extension)
```sql
CREATE EXTENSION IF NOT EXISTS dblink;

select dblink_connect('mydblink','hostaddr=127.0.0.1 port=5432 dbname=test_db user=mydb password=1qaz2wsx')

SELECT * FROM  dblink('hostaddr=127.0.0.1 port=5432 dbname=test_db user=mydb password=1qaz2wsx', 'select * from company2') AS company2(id int, name text, age int, address char, salary real)
```