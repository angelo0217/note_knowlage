# Docker
## install
```shell
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum list docker-ce --showduplicates | sort -r #查看版本
sudo yum install -y docker-ce-19.03.9-3.el7 #選擇stable版

sudo systemctl enable docker

# 安裝有延遲問題，可能導致daemon.json尚未建立。
# Update (Docker Server) 自定義daemon.json 
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "10"
  },
  "storage-driver": "overlay2"
}
EOF
mkdir -p /etc/systemd/system/docker.service.d

# Restart docker
systemctl daemon-reload
systemctl restart docker
systemctl enable docker.service

# 啟動 
sudo systemctl start docker
# 關閉
sudo systemctl stop docker
```
## uninstall
```shell
systemctl stop docker

# Clean docker 
yes | sudo docker system prune --all --volumes

rm -rf /var/lib/docker /etc/docker
rm -rf /var/run/docker.sock
rm -rf /usr/bin/docker-compose

# Uninstall old versions
yes | sudo yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine \
    docker-ce \
    docker-ce-cli 
```
## 設定root以外user，使用docker指令
- sudo usermod -a -G docker albert
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
```shell
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
```shell
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
## 訪問容器
- docker run --rm -it <image name> /bin/bash
- docker exec -it mysql-test /bin/sh
## 常用
### consul 
```shell
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
```shell
docker run --name redis-lab -p 6379:6379 -d redis
```
### Mq
```shell
docker run --name local-mq -p 5672:5672 -p 15672:15672 --restart=always -d rabbitmq:3.8.3-management
```
### portainer
```shell
docker run -d -p 9000:9000 --restart=always --name portainer -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
```
