# Docker 在 WSL2 的安裝指南

本文檔提供了在 WSL2 上安裝和配置 Docker 及 Docker Compose 的詳細步驟。

## 目錄

- [在 WSL2 上安裝 Docker](#在-wsl2-上安裝-docker)
    - [方法1：使用 Docker Desktop（推薦方式）](#方法1使用-docker-desktop推薦方式)
    - [方法2：在 WSL2 中直接安裝 Docker Engine](#方法2在-wsl2-中直接安裝-docker-engine)
- [安裝 Docker Compose](#安裝-docker-compose)
    - [方法1：透過 Docker Desktop（如果已安裝）](#方法1透過-docker-desktop如果已安裝)
    - [方法2：使用 apt 包管理器安裝](#方法2使用-apt-包管理器安裝)
    - [方法3：使用官方安裝腳本（推薦方式）](#方法3使用官方安裝腳本推薦方式)
    - [方法4：使用 pip 安裝](#方法4使用-pip-安裝)
- [Docker Compose 使用基礎範例](#docker-compose-使用基礎範例)

## 在 WSL2 上安裝 Docker

### 方法1：使用 Docker Desktop（推薦方式）

1. 下載並安裝 Docker Desktop for Windows：
    - 訪問 https://www.docker.com/products/docker-desktop
    - 下載 Windows 版 Docker Desktop 安裝程序
    - 運行安裝程序

2. 在安裝過程中，確保選中 "Use WSL 2 instead of Hyper-V" 選項

3. 安裝完成後，打開 Docker Desktop

4. 進入 Docker Desktop 設置，在 "Resources" > "WSL Integration" 中啟用您想要使用 Docker 的 WSL2 發行版

5. 應用設置並重啓 Docker Desktop

6. 打開您的 WSL2 終端，運行 `docker --version` 來驗證安裝

### 方法2：在 WSL2 中直接安裝 Docker Engine

如果您不想使用 Docker Desktop，也可以直接在 WSL2 中安裝 Docker Engine：

1. 打開您的 WSL2 終端

2. 更新包索引：
   ```bash
   sudo apt-get update
   ```

3. 安裝必要的軟件包：
   ```bash
   sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
   ```

4. 添加 Docker 官方 GPG 密鑰：
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

5. 設置穩定版本的 Docker 倉庫：
   ```bash
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

6. 再次更新包索引：
   ```bash
   sudo apt-get update
   ```

7. 安裝 Docker Engine：
   ```bash
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

8. 啟動 Docker 服務：
   ```bash
   sudo service docker start
   ```

9. 將當前用戶添加到 docker 用戶組，以便無需 sudo 運行 docker 命令：
   ```bash
   sudo usermod -aG docker $USER
   ```

10. 重新登錄您的 WSL2 會話，或執行以下命令應用組更改：
    ```bash
    newgrp docker
    ```

11. 驗證安裝：
    ```bash
    docker --version
    docker run hello-world
    ```

## 安裝 Docker Compose

### 方法1：透過 Docker Desktop（如果已安裝）

如果您使用的是 Docker Desktop for Windows 並啟用了 WSL2 整合，Docker Compose 已經預先安裝好了。您可以直接在 WSL2 終端中運行以下命令檢查版本：

```bash
docker compose version
```

### 方法2：使用 apt 包管理器安裝

適用於 Ubuntu/Debian 發行版：

```bash
# 更新包列表
sudo apt-get update

# 安裝 Docker Compose
sudo apt-get install docker-compose-plugin
```

安裝後，驗證安裝：
```bash
docker compose version
```

### 方法3：使用官方安裝腳本（推薦方式）

如果你想安裝最新版本的 Docker Compose，可以使用官方提供的安裝方法：

1. 創建一個目錄來存放下載的二進制文件：
```bash
mkdir -p ~/.docker/cli-plugins/
```

2. 下載最新版本的 Docker Compose（您可以在 [Docker Compose GitHub 發布頁面](https://github.com/docker/compose/releases) 找到最新版本）：
```bash
curl -SL https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
```

3. 使檔案可執行：
```bash
chmod +x ~/.docker/cli-plugins/docker-compose
```

4. 驗證安裝：
```bash
docker compose version
```

### 方法4：使用 pip 安裝

如果您熟悉 Python，也可以使用 pip 安裝 Docker Compose：

```bash
# 安裝 pip（如果尚未安裝）
sudo apt-get install python3-pip

# 安裝 Docker Compose
pip3 install docker-compose
```

驗證安裝：
```bash
docker-compose --version
```

## Docker Compose 使用基礎範例

安裝完成後，您可以通過創建一個簡單的 `docker-compose.yml` 文件來測試 Docker Compose：

```yaml
version: '3'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
```

然後運行：
```bash
docker compose up -d
```

這將啟動一個 Nginx 容器，您可以通過瀏覽器訪問 http://localhost:8080 來測試。

停止服務：
```bash
docker compose down
```

**注意**：從 Docker Compose v2 開始，命令格式已從 `docker-compose` 更改為 `docker compose`（中間有空格）。不過，在某些安裝方式下，兩種命令格式可能都支持。