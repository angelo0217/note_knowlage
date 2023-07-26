# Docker
## wsl fix network
```shell
cat /etc/resolv.conf
sudo nano /etc/resolv.conf
#修改
nameserver 8.8.8.8
```
## remove old version
```shell
sudo apt-get remove docker docker-engine docker.io containerd runc
```
## linux update
```shell
sudo apt-get update
```
## install dependencies
```shell
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```
## add Docker’s official GPG key
```shell
curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```
### Verify that you now have the key with the fingerprint
```shell
sudo apt-key fingerprint 0EBFCD88
```
## set up the stable repository
```shell
sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/ \
  $(lsb_release -cs) \
  stable"
```
## query docker version
```shell
apt-cache madison docker-ce
```
## install docker
```shell
sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
sudo apt-get install docker-ce=5:24.0.5-1~ubuntu.22.04~jammy docker-ce-cli=5:24.0.5-1~ubuntu.22.04~jammy containerd.io
```
