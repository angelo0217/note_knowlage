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
