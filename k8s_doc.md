# Kubernetes (k8s) 與 K3s 安裝與指令整理

## Kubernetes (k8s) 安裝方式

Kubernetes 的安裝方式有多種，以下列出幾種常見的方式：

### 1. 使用 kubeadm 安裝

* **優點：** 官方推薦，靈活度高，可客製化程度高。
* **缺點：** 安裝步驟較繁瑣。
* **步驟：**
    1.  安裝 Docker 或 containerd 等容器運行時。
    2.  安裝 kubeadm、kubelet、kubectl。
    3.  使用 `kubeadm init` 初始化 Master 節點。
    4.  使用 `kubeadm join` 將 Worker 節點加入叢集。
* **適用場景：** 生產環境、需要高度客製化的場景。

### 2. 使用雲端託管服務 (例如：GKE、EKS、AKS)

* **優點：** 安裝簡單，維運成本低，可快速部署。
* **缺點：** 客製化程度受限於雲端供應商。
* **步驟：** 依照雲端供應商提供的文件進行操作。
* **適用場景：** 快速部署、不需要高度客製化的場景。

### 3. 使用 minikube 安裝

* **優點：** 方便在本機端進行開發測試。
* **缺點：** 僅適用於單節點環境。
* **步驟：** 安裝 minikube 後，執行 `minikube start` 即可。
* **適用場景：** 開發測試環境。

## K3s 安裝方式

K3s 是一個輕量級的 Kubernetes 發行版，適合用於資源受限的環境。

### 1. 單節點安裝

* **步驟：**
    1.  執行以下指令：

    ```bash
    curl -sfL [https://get.k3s.io](https://get.k3s.io) | sh -
    ```

    2.  等待安裝完成。
    3.  使用 `kubectl` 指令操作叢集。

### 2. 多節點安裝

* **步驟：**
    1.  在 Master 節點執行單節點安裝指令。
    2.  在 Worker 節點執行以下指令：

    ```bash
    curl -sfL [https://get.k3s.io](https://get.k3s.io) | K3S_URL=https://<Master 節點 IP>:6443 K3S_TOKEN=<Token> sh -
    ```

    * `<Master 節點 IP>`：Master 節點的 IP 位址。
    * `<Token>`：Master 節點產生的 Token，可使用 `sudo cat /var/lib/rancher/k3s/server/node-token` 取得。

## Kubernetes (k8s) 指令

### 基本指令

* `kubectl get pods`：取得 Pod 列表。
* `kubectl get deployments`：取得 Deployment 列表。
* `kubectl get services`：取得 Service 列表。
* `kubectl create deployment <Deployment 名稱> --image=<Image 名稱>`：建立 Deployment。
* `kubectl expose deployment <Deployment 名稱> --port=<Port> --target-port=<Target Port> --type=LoadBalancer`：建立 Service。
* `kubectl delete deployment <Deployment 名稱>`：刪除 Deployment。
* `kubectl delete service <Service 名稱>`：刪除 Service。
* `kubectl apply -f <YAML 檔案>`：套用 YAML 檔案。
* `kubectl describe pod <Pod 名稱>`：取得 Pod 詳細資訊。
* `kubectl logs <Pod 名稱>`：取得 Pod 日誌。
* `kubectl exec -it <Pod 名稱> -- bash`：進入 Pod 內部。

### 進階指令

* `kubectl get nodes`：取得 Node 列表。
* `kubectl get namespaces`：取得 Namespace 列表。
* `kubectl create namespace <Namespace 名稱>`：建立 Namespace。
* `kubectl delete namespace <Namespace 名稱>`：刪除 Namespace。
* `kubectl get secrets`：取得 Secret 列表。
* `kubectl create secret generic <Secret 名稱> --from-literal=<Key>=<Value>`：建立 Secret。
* `kubectl delete secret <Secret 名稱>`：刪除 Secret。
* `kubectl get configmaps`：取得 ConfigMap 列表。
* `kubectl create configmap <ConfigMap 名稱> --from-literal=<Key>=<Value>`：建立 ConfigMap。
* `kubectl delete configmap <ConfigMap 名稱>`：刪除 ConfigMap。

## Kubernetes (k8s) 層級介紹

Kubernetes 的層級結構如下：

### 1. Cluster (叢集)

* **說明：**
    * Kubernetes 叢集是 Kubernetes 的最上層結構，它由多個 Node 組成，共同運行容器化的應用程式。
    * 叢集提供了一個統一的平台，用於管理和協調應用程式的部署、擴展和維護。
* **範例：**
    * 一個 Kubernetes 叢集可能包含數個 Master Node 和多個 Worker Node，這些 Node 可以是實體伺服器或虛擬機器。

### 2. Node (節點)

* **說明：**
    * Node 是 Kubernetes 叢集中的工作機器，負責運行 Pod。
    * Node 分為 Master Node 和 Worker Node 兩種：
        * **Master Node：**
            * 負責控制整個叢集，包括 API 伺服器、排程器和控制器等元件。
            * 管理 Worker Node 並協調應用程式的部署。
        * **Worker Node：**
            * 運行實際的應用程式容器。
            * 由 Master Node 管理，並向 Master Node 報告其狀態。
* **範例：**
    * Master Node：運行 kube-apiserver、kube-scheduler、kube-controller-manager 和 etcd。
    * Worker Node：運行 kubelet 和 kube-proxy。

### 3. Pod (容器組)

* **說明：**
    * Pod 是 Kubernetes 的最小部署單位，可以包含一個或多個容器。
    * Pod 中的容器共享相同的網路命名空間和儲存卷。
    * Pod 提供了一個抽象層，用於管理容器的生命週期。
* **範例：**

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: my-pod
    spec:
      containers:
      - name: my-container
        image: nginx:latest
    ```

### 4. Deployment (部署)

* **說明：**
    * Deployment 用於管理 Pod 的生命週期，確保 Pod 的數量和狀態符合預期。
    * Deployment 可以自動擴展或縮減 Pod 的數量，並在 Pod 發生故障時進行自動恢復。
* **範例：**

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: my-app
      template:
        metadata:
          labels:
            app: my-app
        spec:
          containers:
          - name: my-container
            image: nginx:latest
    ```

### 5. Service (服務)

* **說明：**
    * Service 提供了一個穩定的網路存取點，讓應用程式可以被其他應用程式或外部用戶存取。
    * Service 可以將流量路由到一組 Pod，並提供負載平衡和服務發現功能。
* **範例：**

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: my-service
    spec:
      selector:
        app: my-app
      ports:
      - protocol: TCP
        port: 80
        targetPort: 80
    ```

### 6. Namespace (命名空間)

* **說明：**
    * Namespace 將叢集資源進行邏輯隔離，用於將不同的應用程式或團隊分隔開來。
    * Namespace 提供了一種資源管理和存取控制的機制。
* **範例：**
    * 可以創建一個 "development" Namespace 和一個 "production" Namespace，用於隔離開發環境和生產環境。

### 7. Secret (機密)

* **說明：**
    * Secret 用於儲存敏感資訊，例如密碼、API 金鑰等。
    * Secret 將敏感資訊與應用程式程式碼分離，提高了應用程式的安全性。
* **範例：**
    * 可以使用 Secret 儲存資料庫的密