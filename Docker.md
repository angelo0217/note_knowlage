# Docker 學習筆記

這是一份關於 Docker 的學習筆記，涵蓋了核心概念、安裝、常用指令及設定範例。

## 1. 核心概念

在開始之前，先了解 Docker 的幾個核心元件：

- **映像檔 (Image)**: 一個唯讀的模板，包含了執行應用程式所需的所有內容，例如程式碼、函式庫、環境變數和設定檔。映像檔是建立容器的基礎。
- **容器 (Container)**: 映像檔的執行中實例。容器是獨立、輕量級的執行環境，可以被輕易地啟動、停止、移動和刪除。容器之間互相隔離。
- **資料卷 (Volume)**: 用於持久化保存容器資料的機制。資料卷會繞過容器的檔案系統，直接將資料儲存在主機上，避免容器被刪除時資料遺失。
- **倉庫 (Repository)**: 集中存放映像檔的地方。最知名的公開倉庫是 [Docker Hub](https://hub.docker.com/)。

---

## 2. 安裝與設定 (CentOS)

### 2.1. 安裝 Docker

```shell
# 1. 安裝所需的工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# 2. 新增 Docker 的軟體源
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 3. (可選) 查看所有可用的 Docker 版本
sudo yum list docker-ce --showduplicates | sort -r

# 4. 安裝指定版本的 Docker (建議選擇 stable 版)
sudo yum install -y docker-ce-19.03.9-3.el7

# 5. 啟動 Docker 服務
sudo systemctl start docker

# 6. 設定開機自動啟動
sudo systemctl enable docker
```

### 2.2. 移除 Docker

```shell
# 1. 停止 Docker 服務
sudo systemctl stop docker

# 2. 移除所有 Docker 元件 (容器、映像檔、網路、資料卷)
yes | sudo docker system prune --all --volumes

# 3. 移除 Docker 相關套件
yes | sudo yum remove docker-ce docker-ce-cli containerd.io

# 4. 刪除 Docker 相關目錄
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

### 2.3. 使用者權限設定

為了避免每次執行 `docker` 指令都需要加上 `sudo`，可以將目前使用者加入 `docker` 群組。

```shell
# 將目前使用者加入 docker 群組 (albert 請替換成你的使用者名稱)
sudo usermod -aG docker albert

# 執行後需要重新登入或重開機才會生效
```

### 2.4. 設定 Daemon (daemon.json)

Docker 的核心服務設定檔位於 `/etc/docker/daemon.json`。如果檔案不存在，可以手動建立。

以下是一個推薦的基礎設定範例：

```shell
# 建立並寫入設定
sudo cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "10"
  },
  "storage-driver": "overlay2",
  "registry-mirrors": [
    "https://hub-mirror.c.163.com"
  ]
}
EOF

# 重新載入設定並重啟 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

- `exec-opts`: 配合 systemd，是 Kubernetes 的推薦設定。
- `log-driver` & `log-opts`: 設定日誌輪替，避免日誌檔無限制增長佔滿硬碟。
- `storage-driver`: 儲存驅動，`overlay2` 是目前推薦的選項。
- `registry-mirrors`: 設定鏡像加速器，可大幅提升下載公開映像檔的速度。

---

## 3. 常用指令

### 3.1. 容器管理

```shell
# 顯示目前正在執行的容器
docker ps

# 顯示所有容器 (包含已停止的)
docker ps -a

# 執行一個新容器 (-d: 背景執行, -p: 映射連接埠, --name: 命名)
docker run -d -p 8080:80 --name my-web-server nginx

# 停止一個容器
docker stop my-web-server

# 啟動一個已停止的容器
docker start my-web-server

# 移除一個容器 (需先停止)
docker rm my-web-server

# 強制移除一個執行中的容器
docker rm -f my-web-server

# 進入一個執行中的容器並開啟互動式終端機
# (適合用來偵錯或查看容器內部狀態)
docker exec -it my-web-server /bin/bash

# 查看容器的日誌
docker logs my-web-server

# 持續追蹤容器的日誌
docker logs -f my-web-server
```

### 3.2. 映像檔管理

```shell
# 顯示本機所有的映像檔
docker images

# 從倉庫下載映像檔
docker pull nginx:latest

# 移除本機的映像檔
docker rmi nginx:latest

# 移除所有未被使用的映像檔
docker image prune -a
```

### 3.3. 系統管理

```shell
# 顯示 Docker 系統資訊
docker info

# 顯示所有容器的即時資源使用狀況
docker stats

# 移除所有已停止的容器、未使用的網路和懸空的映像檔
docker system prune

# (危險) 移除所有未使用的容器、網路、映像檔和資料卷
yes | docker system prune -a --volumes
```

---

## 4. Docker 網路

Docker 提供多種網路模式，讓容器能與外部世界或其他容器溝通。預設情況下，Docker 會建立一個名為 `bridge` 的虛擬網路。

### 4.1. Bridge Mode (橋接模式)

- **這是 Docker 的預設網路模式。**
- Docker 會建立一個私有的內部網路，所有在此網路中的容器都可以透過 IP 位址互相通訊。
- 如果要讓外部存取容器的服務，需要透過 `-p` 或 `-P` 參數將容器的連接埠映射到主機上。
- **優點**: 容器之間互相隔離，安全性較高。
- **缺點**: 網路效能相較於 Host 模式稍差，因為需要經過 NAT (網路位址轉換)。

```shell
# 執行一個使用 bridge 模式的容器 (預設行為)
# 將主機的 8080 port 映射到容器的 80 port
docker run -d -p 8080:80 --name web_bridge nginx
```

### 4.2. Host Mode (主機模式)

- 容器不會擁有自己獨立的網路命名空間，而是直接共享主機的網路。
- 容器會直接使用主機的 IP 位址和連接埠，因此不需要進行連接埠映射。
- **優點**: 網路效能最佳，因為它移除了 NAT 的環節。
- **缺點**: 安全性較低，因為容器直接暴露在主機網路上，且可能與主機上的服務產生連接埠衝突。

```shell
# 執行一個使用 host 模式的容器
# 容器內的應用程式可以直接監聽主機的 80 port
docker run -d --network=host --name web_host nginx
```

### 4.3. None Mode (無網路模式)

- 容器擁有自己的網路命名空間，但不會進行任何網路設定。
- 容器內只有一個 `lo` (loopback) 網路介面，無法與外部或其他容器通訊。
- **適用情境**: 適用於只需要處理資料而不需要網路連線的任務。

```shell
# 執行一個沒有網路的容器
docker run -it --network=none --name no_net_container busybox
```

### 4.4. 網路相關指令

```shell
# 列出所有網路
docker network ls

# 建立一個自訂的 bridge 網路
docker network create my-custom-network

# 查看特定網路的詳細資訊
docker network inspect my-custom-network

# 讓容器連接到指定的網路
docker network connect my-custom-network web_bridge
```

---

## 5. Dockerfile 與映像檔

`Dockerfile` 是一個用來建構映像檔的腳本檔案。

```dockerfile
# Dockerfile 範例
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

### 5.1. 建構與匯出

```shell
# 從 Dockerfile 建構映像檔
docker build -t my-python-app .

# 將映像檔匯出成 tar 檔 (方便在沒有網路的環境中部署)
docker save -o my-python-app.tar my-python-app:latest

# 從 tar 檔載入映像檔
docker load -i my-python-app.tar
```

---

## 6. Docker Compose

`Docker Compose` 是一個用來定義和執行多容器 Docker 應用程式的工具。透過一個 `docker-compose.yml` 檔案，就可以設定所有應用程式的服務。

### 6.1. 常用指令

```shell
# 根據 docker-compose.yml 啟動所有服務 (背景執行)
docker-compose up -d

# 停止並移除所有服務、網路、資料卷
docker-compose down --volumes

# 完整重建：停止並移除舊的，然後重新建構並啟動
docker-compose down --volumes --remove-orphans && docker-compose up -d --build
```

---

## 7. 常用服務範例

### Portainer (圖形化管理介面)

```shell
docker run -d -p 9000:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```

### Redis

```shell
docker run -d -p 6379:6379 --name redis-lab --restart=always redis
```

### RabbitMQ

```shell
docker run -d -p 5672:5672 -p 15672:15672 --name local-mq --restart=always rabbitmq:3.8-management
```

### Consul

```shell
docker run -d --name=consul-server -p 8500:8500 --restart=always consul agent -server -bootstrap-expect=1 -ui -data-dir=/consul/data -client=0.0.0.0
```

---

## 8. 進階設定 (daemon.json 參考)

以下是一些 `daemon.json` 中常用選項的說明。完整的選項清單請參考 [官方文件](https://docs.docker.com/engine/reference/commandline/dockerd/)。

- `debug`: `true` / `false` - 啟用除錯模式。
- `hosts`: `[]` - 綁定 Docker 服務監聽的地址，例如 `["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]`。
- `log-level`: `"info"` - 設定日誌等級 (debug, info, warn, error, fatal)。
- `insecure-registries`: `[]` - 設定允許使用 HTTP 連線的私有倉庫地址。
- `registry-mirrors`: `[]` - 設定倉庫鏡像，加速映像檔下載。
- `data-root`: `"/var/lib/docker"` - 更改 Docker 的資料儲存根目錄。
- `storage-opts`: `[]` - 儲存驅動的相關選項，例如 `["size=50GB"]`。

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
