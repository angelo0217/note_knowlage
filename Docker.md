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

- docker run --rm -it $image_name /bin/bash
- docker exec -it $container_name /bin/sh

## 顯示容器使用資源
- docker ps -q | xargs docker stats

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

# save image for Containerd

```shell
docker save -o demo-spring.tar demo-spring:0.0.1
```

# Docker [備忘錄](https://mp.weixin.qq.com/s/iquAB8g5zyb8A2ReiQ3RSQ)

## daemon

```json
{
    "api-cors-header": "",
    //在引擎API中设置CORS标头
    "authorization-plugins": [],
    //要加载的授权插件
    "bridge": "",
    //将容器附加到网桥
    "cgroup-parent": "",
    //为所有容器设置父cgroup
    "cluster-store": "",
    // 分布式存储后端的URL
    "cluster-store-opts": {},
    //设置集群存储选项（默认map []）
    "cluster-advertise": "",
    //要通告的地址或接口名称
    "debug": true,
    //启用调试模式，启用后，可以看到很多的启动信息。默认false
    "default-gateway": "",
    //容器默认网关IPv4地址
    "default-gateway-v6": "",
    //容器默认网关IPv6地址
    "default-runtime": "runc",
    //容器的默认OCI运行时（默认为“ runc"）
    "default-ulimits": {},
    //容器的默认ulimit（默认[]）
    "dns": [
        "192.168.1.1"
    ],
    //设定容器DNS的地址，在容器的 /etc/resolv.conf文件中可查看。
    "dns-opts": [],
    //容器 /etc/resolv.conf 文件，其他设置
    "dns-search": [],
    //设定容器的搜索域，当设定搜索域为 .example.com 时，在搜索一个名为 host 的 主机时，DNS不仅搜索host，还会搜索host.example.com 。 注意：如果不设置， Docker 会默认用主机上的 /etc/resolv.conf 来配置容器。
    "exec-opts": [],
    //运行时执行选项
    "exec-root": "",
    //执行状态文件的根目录（默认为’/var/run/docker‘）
    "fixed-cidr": "",
    //固定IP的IPv4子网
    "fixed-cidr-v6": "",
    //固定IP的IPv6子网
    "data-root": "/var/lib/docker",
    //Docker运行时使用的根路径，默认/var/lib/docker
    "group": "",
    //UNIX套接字的组（默认为“docker"）
    "hosts": [],
    //设置容器hosts
    "icc": false,
    //启用容器间通信（默认为true）
    "ip": "0.0.0.0",
    //绑定容器端口时的默认IP（默认0.0.0.0）
    "iptables": false,
    //—启用iptables规则添加（默认为true）
    "ipv6": false,
    //启用IPv6网络
    "ip-forward": false,
    //默认true, 启用 net.ipv4.ip_forward,进入容器后使用 sysctl -a | grepnet.ipv4.ip_forward 查看
    "ip-masq": false,
    //启用IP伪装（默认为true）
    "labels": [
        "nodeName=node-121"
    ],
    //docker主机的标签，很实用的功能,例如定义：–label nodeName=host-121
    "live-restore": true,
    //在容器仍在运行时启用docker的实时还原
    "log-driver": "",
    //容器日志的默认驱动程序（默认为“ json-file"）
    "log-level": "",
    //设置日志记录级别（“调试"，“信息"，“警告"，“错误"，“致命"）（默认为“信息"）
    "max-concurrent-downloads": 3,
    //设置每个请求的最大并发下载量（默认为3）
    "max-concurrent-uploads": 5,
    //设置每次推送的最大同时上传数（默认为5）
    "mtu": 0,
    //设置容器网络MTU
    "oom-score-adjust": -500,
    //设置守护程序的oom_score_adj（默认值为-500）
    "pidfile": "",
    //Docker守护进程的PID文件
    "raw-logs": false,
    //全时间戳机制
    "selinux-enabled": false,
    //默认 false，启用selinux支持
    "storage-driver": "",
    //要使用的存储驱动程序
    "swarm-default-advertise-addr": "",
    //设置默认地址或群集广告地址的接口
    "tls": true,
    //默认 false, 启动TLS认证开关
    "tlscacert": "",
    //默认 ~/.docker/ca.pem，通过CA认证过的的certificate文件路径
    "tlscert": "",
    //默认 ~/.docker/cert.pem ，TLS的certificate文件路径
    "tlskey": "",
    //默认~/.docker/key.pem，TLS的key文件路径
    "tlsverify": true,
    //默认false，使用TLS并做后台进程与客户端通讯的验证
    "userland-proxy": false,
    //使用userland代理进行环回流量（默认为true）
    "userns-remap": "",
    //用户名称空间的用户/组设置
    "bip": "192.168.88.0/22",
    //——指定网桥IP
    "registry-mirrors": [
        "https://192.498.89.232:89"
    ],
    //设置镜像加速
    "insecure-registries": [
        "120.123.122.123:12312"
    ],
    //—设置私有仓库地址可以设为http
    "storage-opts": [
        "overlay2.override_kernel_check=true",
        "overlay2.size=15G"
    ],
    //存储驱动程序选项
    "log-opts": {
        "max-file": "3",
        "max-size": "10m"
    },
    //容器默认日志驱动程序选项
    "iptables": false
    //启用iptables规则添加（默认为true）
}

```

### docker container ping
```shell
docker exect -it {container name 1} ping {container name 2}
```
### [container ping install](https://blog.csdn.net/qq_37960603/article/details/110294270)