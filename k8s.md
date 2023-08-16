# k8s
#Set Hostname on master Nodes
```shell
hostnamectl set-hostname master-node
vi /etc/hosts
10.0.2.15 master-node
10.0.2.20 worker-node
```

#Set Hostname on worker Nodes
```shell
hostnamectl set-hostname worker-node1
vi /etc/hosts
10.0.2.10 master-node
10.0.2.20 worker-node
```
# install bash
```shell
yum -y install bash-completion
source /etc/profile
```
# disabled firewalld
```shell
systemctl stop firewalld.service 
systemctl disable firewalld.service
```
#Configure Firewall on master node
```shell
firewall-cmd --permanent --add-port=6443/tcp
firewall-cmd --permanent --add-port=2379-2380/tcp
firewall-cmd --permanent --add-port=10250/tcp
firewall-cmd --permanent --add-port=10251/tcp
firewall-cmd --permanent --add-port=10252/tcp
firewall-cmd --permanent --add-port=10255/tcp
firewall-cmd --reload
```
#Configure Firewall on worker node
```shell
firewall-cmd --permanent --add-port=10251/tcp
firewall-cmd --permanent --add-port=10255/tcp
firewall-cmd --reload
```
# Disable SELinux
```shell
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```
#Disable SWAP
```shell
free -h
sudo swapoff -a
sudo sed -i 's/.*swap.*/#&/' /etc/fstab
free -h
```
## install containerd
```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo 
sudo yum install -y containerd.io

systemctl stop containerd.service

cp /etc/containerd/config.toml /etc/containerd/config.toml.bak
sudo containerd config default > $HOME/config.toml
sudo cp $HOME/config.toml /etc/containerd/config.toml
# 修改 /etc/containerd/config.toml 文件后，要将 docker、containerd 停止后，再启动
sudo sed -i "s#registry.k8s.io/pause#registry.cn-hangzhou.aliyuncs.com/google_containers/pause#g" /etc/containerd/config.toml
# https://kubernetes.io/zh-cn/docs/setup/production-environment/container-runtimes/#containerd-systemd
# 确保 /etc/containerd/config.toml 中的 disabled_plugins 内不存在 cri
sudo sed -i "s#SystemdCgroup = false#SystemdCgroup = true#g" /etc/containerd/config.toml

#启动containerd
systemctl start containerd.service
systemctl status containerd.service
```

##Configure Kubernetes Repository
```shell
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
```
##Install kubelet, kubeadm, and kubectl
```shell
K8S_VERSION='1.26.2-0'
yum install -y kubelet-$K8S_VERSION kubeadm-$K8S_VERSION kubectl-$K8S_VERSION

systemctl daemon-reload
systemctl enable kubelet
systemctl start kubelet
```
##将桥接的 IPv4 流量传递到 iptables 的链
```shell
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
modprobe br_netfilter
echo 1 > /proc/sys/net/ipv4/ip_forward
```


## Create Cluster with kubeadm - master [參考](https://blog.frognew.com/2023/01/kubeadm-install-kubernetes-1.26.html)
```shell
cat > /opt/config.yaml <<EOF
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 10.0.2.15
  bindPort: 6443
nodeRegistration:
  criSocket: unix:///run/containerd/containerd.sock
  taints:
  - effect: PreferNoSchedule
    key: node-role.kubernetes.io/master
---
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: 1.26.2
imageRepository: registry.aliyuncs.com/google_containers
networking:
  podSubnet: 10.244.0.0/16
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
failSwapOn: false
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: ipvs
EOF

kubeadm init --config=/opt/config.yaml --ignore-preflight-errors=all

echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile
source ~/.bash_profile

kubectl get node
# 預設Master Node無法部署Pod
kubectl taint nodes --all node-role.kubernetes.io/master-
#查詢 join command
kubeadm token create --print-join-command
```
# join cluster -- worker node
```shell
#來源會是上面跑完的
kubeadm join 192.168.19.135:6443 --token i7w5xr.u3t483h07aksnzg6 \
	--discovery-token-ca-cert-hash sha256:04defa4d856cb5bcfe7ad0c3f2d71aa7d48e6c27e4e5821336db00c1e4bf7464
```
# Network [參考](https://ithelp.ithome.com.tw/m/articles/10295266)
## 第一種 kube-flannel.yml
```shell
#查看各節點狀態
kubectl describe nodes
# 查看 cidr
kubectl cluster-info dump | grep -m 1 cluster-cidr
#會看到類似   "--cluster-cidr=192.168.0.0/16",
wget https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
vi kube-flannel.yml # 調整 Network 等於上面
#kind: ConfigMap
#apiVersion: v1
#metadata:
#  name: kube-flannel-cfg
#  ...
#data:
#  ...
#  net-conf.json: |
#    {
#      "Network": "192.168.0.0/16",
#      "Backend": {
#        "Type": "vxlan"
#      }
#    }
    
kubectl apply -f kube-flannel.yml
```
### 修正 open /run/flannel/subnet.env: no such file or directory[參考](https://www.jianshu.com/p/9819a9f5dda0)
```shell
# 檢查是否有下面的env file
vi /run/flannel/subnet.env
#輸入以下要對其上面的network
FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.0.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
```
## 第二種 calico
```shell
wget https://raw.githubusercontent.com/projectcalico/calico/v3.24.1/manifests/calico.yaml
#calico 會自行調整內容，無須調整
kubectl apply -f calico.yaml
kubectl get pods -A
```

# create namespace
```shell
kubectl create namespace fz-k8s
```
#NodePort 
 - 端口范围是 30000 到 32767
#test nginx [參考](https://www.cnblogs.com/Fzeng/p/17288286.html) 
```shell
cat > nginx.yaml << EOF
# 创建命名空间  ：kubectl create namespace fz-k8s
# 创建 pod    ：kubectl apply -f nginx-deployment.yaml
# 查看 pod    ：kubectl -n fz-k8s get pod -o wide
# 查看 pod    ：kubectl -n fz-k8s get pod -o wide
# 进入 pod    ：kubectl -n fz-k8s exec -it pod名称 bash
# 编辑 pod    ：kubectl -n fz-k8s edit deployment nginx-deployment
# 删除 pod    ：kubectl -n fz-k8s delete deployment nginx-deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: fz-k8s
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.23.2
        ports:
        - containerPort: 80
---
# 创建 Service（不能指定 nodePort） ：kubectl -n zlm-k8s expose deployment nginx-deployment --type=NodePort --name=nginx-service
# 编辑 Service                    ：kubectl -n zlm-k8s edit service nginx-service
# 删除 Service                    ：kubectl -n zlm-k8s delete service nginx-service
# 查看 pod、Service               ：kubectl -n 命名空间 get pod,svc -o wide

# https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: fz-k8s
spec:
  ports:
    - nodePort: 30080
      port: 80
      protocol: TCP
      targetPort: 80
  selector:
    app: nginx
  type: NodePort
EOF

kubectl apply -f nginx.yaml
kubectl delete -f nginx.yaml

kubectl get services -o wide -n fz-k8s
kubectl get deployment -n fz-k8s
#查看所有節點
kubectl describe nodes

#查看容器log
kubectl logs <pod-name> -c <container-name> -n <namespace>
kubectl logs nginx-deployment -c nginx-deployment-565887c86b-bnwvw -n fz-k8s
kubectl logs POD_NAME -c demo-mysql
訪問容器
kubectl exec -it POD_NAME -c demo-mysql -- /bin/bash


kubectl describe pod <pod-name> -n <namespace>

kubectl get pods -n fz-k8s
kubectl describe pod nginx-deployment-565887c86b-hsvxj -n fz-k8s
kubectl get events -n fz-k8s
# 查看 pod 跟 容器名稱
kubectl get pods --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,POD:.metadata.name,CONTAINERS:.spec.containers[*].name"

kubectl describe pod calico-kube-controllers-5f94594857-555vz -n kube-system

```
# helm
```shell
mkdir myhelm
cd myhelm
curl -SLO https://get.helm.sh/helm-v3.12.2-linux-amd64.tar.gz
tar -zxvf helm-v3.12.2-linux-amd64.tar.gz
mv  linux-amd64/helm  /usr/local/bin/helm
helm version
```
#Dashboard
## 暫時放著，因為沒有token的問題，還找不到解法
```shell
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

vi recommended.yaml change to NodePort
#kind: Service
#apiVersion: v1
#metadata:
#  labels:
#    k8s-app: kubernetes-dashboard
#  name: kubernetes-dashboard
#  namespace: kubernetes-dashboard
#spec:
#  ports:
#    - port: 443
#      targetPort: 8443
#  selector:
#    k8s-app: kubernetes-dashboard
#  type: NodePort
#查看 dashboard port

kubectl apply -f recommended.yaml
kubectl get svc --all-namespaces
# create service account
kubectl create sa cluster-admin-aa -n kubernetes-dashboard

cat > /opt/cluster-admin-aa.yaml <<EOF
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cluster-admin-binding
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: cluster-admin-aa
  namespace: kubernetes-dashboard
EOF

kubectl create -f /opt/cluster-admin-aa.yaml

kubectl get sa cluster-admin-aa -n kubernetes-dashboard -o=yaml

kubectl describe serviceaccount default -n kubernetes-dashboard

# edit to NodePort
```
