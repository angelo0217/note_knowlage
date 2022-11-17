# DockerCompose

## 版本

- https://github.com/docker/compose/releases

## install

```shell
# Install Compose on Linux systems
curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose

# Apply executable permissions to the binary
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

groupadd docker
gpasswd -a ${MANAGER_USER} docker
```

## 啟動 compose file

```shell
docker-compose -f docker-compose.yml up -d
```

## 執行多個compose file

```shell
docker-compose \
    -f docker-compose.yml \
    -f docker-compose.override.yml \
    up
```

## local-vm compose yaml

```shell
version: "3.7"
services:
  qsfmq:
    image: rabbitmq:3.8.3-management
    restart: always
    ports:
      - 5672:5672
      - 15672:15672
  qsf-consul:
    image: consul:1.7.3
    hostname: qsf-consul
    restart: always
    ports:
      - '8300:8300'
      - '8301:8301'
      - '8301:8301/udp'
      - '8500:8500'
      - '8600:8600'
      - '8600:8600/udp'
    command: [ "agent", "-data-dir=/tmp/consul", "-server", "-ui", "-bootstrap", "-datacenter=dc1", "-client=0.0.0.0", "-bind={{ GetInterfaceIP \"eth0\" }}", "-node=server1"]
    networks:
       - byfn
  qsf-redis:
    image: "redis:5.0.8-alpine"
    restart: always
    ports:
      - "6379:6379"
    networks:
      - byfn
networks:
  byfn:
    name: byfn
    driver: overlay
```

## nginx sample

```shell
version: "3.7"
services:
   nginx:
     image: nginx:1.17.10
     extra_hosts:
      qsf-admin: 172.20.111.174
      qfs-mysql: 172.20.111.171
     ports:
       - mode: host
         protocol: tcp
         published: 8520
         target: 8520
       - mode: host
         protocol: tcp
         published: 8530
         target: 8530
     volumes:
       - "/opt/composefile/nginx/nginx.conf:/etc/nginx/nginx.conf"
       - "/opt/composefile/nginx/conf.d:/etc/nginx/conf.d"
       # 左邊主機，右邊容器
```

## mysql

```shell
version: '3.7'
services:
  mysql:
    image: mysql:8.0.25
    container_name: mysql
    command: mysqld --default-authentication-plugin=mysql_native_password --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    ports:
      - '3306:3306'
    environment:
      #      MYSQL_USER: root
      MYSQL_ROOT_PASSWORD: Java1234!
      MYSQL_DATABASE: mydb
```
