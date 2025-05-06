# 在 Windows 上使用 WSL 安裝 Podman 並啟動 Nginx 範例

這份文件整理了在 Windows 環境下，透過 Windows Subsystem for Linux (WSL) 安裝 Podman，並啟動一個簡單的 Nginx "Hello World" 範例的步驟，以及如何找到 WSL 的預設路徑。

## 第一部分：安裝 Windows Subsystem for Linux (WSL)

### 使用單一命令 (適用於 Windows 10 版本 2004 及更高版本，以及 Windows 11)

1.  以管理員身分開啟 PowerShell 或命令提示字元 (CMD)。
2.  執行以下命令：
    ```powershell
    wsl --install
    ```
3.  等待安裝完成並重新啟動你的電腦。
4.  重新啟動後，會開啟一個終端機視窗，要求你設定 Linux 使用者名稱和密碼。

### 手動啟用 WSL 功能並安裝 Linux 發行版 (適用於較舊版本或需要更精細控制)

1.  **啟用 WSL 功能：**
    ```powershell
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
    ```
    重新啟動你的電腦。
2.  **下載並安裝 Linux 發行版：**
    * 開啟 Microsoft Store 並搜尋你想要的 Linux 發行版 (例如 Ubuntu)。
    * 點擊 "取得" 或 "安裝" 並完成安裝後點擊 "啟動"。
    * 設定你的 Linux 使用者名稱和密碼。
3.  **更新到 WSL 2 (強烈建議)：**
    ```powershell
    wsl --set-default-version 2
    wsl --list --verbose # 查看已安裝的發行版及其版本
    wsl --set-version <YourDistroName> 2 # 將特定發行版設定為 WSL 2
    ```

## 第二部分：在 WSL 中安裝 Podman

1.  啟動你的 Linux 發行版 (例如 Ubuntu)。
2.  更新套件列表：
    ```bash
    sudo apt update
    ```
3.  安裝 Podman：
    ```bash
    sudo apt install -y podman
    ```
    如果遇到 `E: Package 'podman' has no installation candidate` 錯誤，請嘗試：
    ```bash
    sudo add-apt-repository universe
    sudo apt update
    sudo apt install -y podman
    ```
4.  驗證安裝：
    ```bash
    podman --version
    ```

## 第三部分：使用 Podman 啟動 Nginx "Hello World" 範例

1.  **建立自訂的 Nginx 配置檔案 (`nginx.conf`)：**
    ```nginx
    server {
        listen 80;
        server_name localhost;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
    ```

2.  **建立 `index.html` 檔案：**
    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello World from Podman!</title>
    </head>
    <body>
        <h1>Hello World from Podman!</h1>
    </body>
    </html>
    ```

3.  **建立 `Dockerfile`：**
    ```dockerfile
    FROM docker.io/nginx:latest
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    COPY index.html /usr/share/nginx/html/
    EXPOSE 80
    ```

4.  **使用 Podman 建構鏡像：**
    ```bash
    podman build -t my-hello-nginx .
    ```
    如果遇到 `short-name ... did not resolve` 錯誤，請確保 `FROM` 行使用完整的 `docker.io/nginx:latest`。

5.  **使用 Podman 運行容器：**
    ```bash
    podman run -d -p 8080:80 --name hello-nginx localhost/my-hello-nginx:latest
    ```
    如果遇到 `short-name ... did not resolve` 錯誤，請使用 `localhost/my-hello-nginx:latest` 或使用 `podman images` 找到 IMAGE ID 並使用 ID 運行。

6.  **在瀏覽器中查看結果：** 打開你的 Windows 瀏覽器，輸入 `localhost:8080`。

7.  **停止和移除容器 (可選)：**
    ```bash
    podman stop hello-nginx
    podman rm hello-nginx
    ```

8.  **移除鏡像 (可選)：**
    ```bash
    podman rmi my-hello-nginx
    ```

## 第四部分：尋找 WSL 的預設路徑

### 在 WSL 終端機內

預設路徑是你的 Linux Home 目錄，通常是：可以使用 `pwd` 命令查看。

### 從 Windows 存取 WSL 檔案系統

1.  開啟檔案總管。
2.  在網址列輸入 `\\wsl$` 並按下 Enter。
3.  你會看到已安裝的 Linux 發行版的資料夾。進入相應的發行版資料夾，你的 Linux Home 目錄位於：

    ```
    \\wsl$\<你的發行版名稱>\home\<你的 Linux 使用者名稱>\
    ```

    在較新的 Windows 版本中，也可以使用：

    ```
    \\wsl.localhost\<你的發行版名稱>\home\<你的 Linux 使用者名稱>\
    ```

這份 Markdown 檔案涵蓋了我們討論的從安裝 WSL 到使用 Podman 啟動範例，以及找到 WSL 預設路徑的各個方面。你可以將其保存為 `.md` 檔案並在支援 Markdown 的閱讀器中查看。