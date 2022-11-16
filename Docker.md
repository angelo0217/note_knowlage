# Docker
## Volumn 預設位置
- /var/lib/docker/volumes
## 取IP
- host.docker.internal
## 清除不必要的Docker image container
- yes | sudo docker system prune -a
## Docker 資源使用
- docker stats --all e5d1187c12d7
- https://docs.docker.com/engine/reference/commandline/stats/
## systemctl
### 擴大空間
```sh
cat > /etc/docker/daemon.json <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts" :[
      "size=50GB"
  ]
}
```
``` sh
{
  "debug": true,
  "experimental": true,
  "exec-opts": ["native.cgroupdriver=systemd"],
  "metrics-addr": "10.140.0.2:9323",
  "insecure-registries": ["java-harbor:10011"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "10"
  },
  "storage-driver": "overlay2"
}
```
## 常用
### consul 
```sh
docker run -d --name=server1 --restart=always \
             -p 8300:8300 \
             -p 8301:8301 \
             -p 8301:8301/udp \
             -p 8302:8302/udp \
             -p 8302:8302 \
             -p 8400:8400 \
             -p 8500:8500 \
             -p 8600:8600 \
             consul agent -server -bind=127.0.0.1 -datacenter=dc1 -bootstrap \
             -data-dir=/tmp/data-dir -client 0.0.0.0 -ui -node=server1
```
### Redis
```sh
docker run --name redis-lab -p 6379:6379 -d redis
```
### Mq
```sh
docker run --name local-mq -p 5672:5672 -p 15672:15672 --restart=always -d rabbitmq:3.8.3-management
```
### portainer
```sh
docker run -d -p 9000:9000 --restart=always --name portainer -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
```
## local-vm compose yaml
```
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
