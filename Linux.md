# 首次安裝開啟網卡
vim /etc/sysconfig/network-scripts/ifcfg-eth0
```shell
ONBOOT=yes
```
```shell
yum install -y net-tools
```

# 安裝ssh
```shell
yum –y install openssh-server openssh-clients
systemctl start sshd
systemctl status sshd
```
# 查硬碟空間

- df -l -h  >>  overlay 查看
- du -shc /opt/*
- docker system df

# 校正時區

- yum -y install ntp
- ntpdate time.stdtime.gov.tw

# 網卡順序

- ip addr

# 權限

- chmod 777 -R /opt/test
- 7
-
    - 4 讀
-
    - 2 寫
-
    - 1 執行
第一个数字（7）代表所有者的权限。它具有最高级别的权限。

7 表示读取（r，4）+写入（w，2）+执行（x，1）的权限。换句话说，所有者可以读取、写入和执行该文件或目录。
第二个数字（7）代表与文件或目录相关的用户组的权限。

7 表示读取（r，4）+写入（w，2）+执行（x，1）的权限。用户组成员可以读取、写入和执行该文件或目录。
第三个数字（7）代表其他用户（非所有者和非用户组成员）的权限。

7 表示读取（r，4）+写入（w，2）+执行（x，1）的权限。其他用户可以读取、写入和执行该文件或目录。
这种权限设置（777）会授予所有用户对文件或目录的最高权限，包括读取、写入和执行。请注意，使用这种权限设置可能会对系统的安全性造成风险，因为它允许任何用户都可以访问和修改文件或目录。在实际使用中，应根据实际需求设置适当的权限。

# linux 系統log

## 等級

- 0: emerg
- 1:alert
- 2:crit
- 3:err
- 4:warning
- 5:notice
- 6:info
- 7:debug

## 範例

```shell
sudo journalctl -p 4 --since 2020-05-29 --until 2020-06-01
journalctl -p 4 --since 2020-09-02 --until 2020-09-04
journalctl -p 7 --since "2021-10-08 12:18:00" --until "2021-10-08 12:20:00"
journalctl -p 6 --since 2020-06-09 --until 2020-06-10
```

# 刪除PID

- ps aux | grep yum
- kill -9 *

# 系統排程

- tail -f /var/log/cron

```shell
centOs 突發cpu暴漲問題
https://blog.csdn.net/weixin_43380635/article/details/91457330
```

# CentOs7 關閉update

```shell
centOs7 關閉update	https://www.itread01.com/content/1511606312.html
https://www.qiuvps.com/1188.html
sudo service yum-cron start
vi /etc/yum/yum-cron.conf
download_updates = yes  改為 no
sudo systemctl stop yum-cron.service
sudo systemctl status yum-cron.service
# Edit download_updates = yes to no
vim /etc/yum/yum-cron.conf
```

# SSH key

- ssh-keygen -t rsa -b 2048 -C 'comment' -f $HOME/.ssh/id_rsa -N ''
- 路徑會產生再 ~/.ssh

### openssh for git
- ssh-keygen -t rsa -b 2048 -C 'comment' -f D:\qsf\gcp\ssh\id_rsa -N ''
- id_rsa.pub內容 完整貼上gitlab

### RSA for jenkins
- ssh-keygen -m PEM -t rsa -b 2048 -C 'comment' -f D:\qsf\gcp\ssh\id_rsa
- id_rsa 貼上jenins ssh type not username pwd

### 服務間ssh連線
- 將產生公鑰放進鑰連線的機器
- vi ~/.ssh/authorized_keys
- id_rsa.pub 內容貼上

### 設定連線 github
id_rsa.pub 複製到 github 的 SSH Keys 設定頁面
id_rsa 保留在 ~/.ssh/內，一般為 /{user_name}/.ssh/id_rsa
chmod 400 ~/.ssh/id_rsa
就可以clone
# 多檔搜尋 GREP

```shell
在 /etc/*.conf 中搜尋 Centos 關鍵字
grep Centos /etc/*.conf
篩選含有 Centos 關鍵字的檔案名稱
ls /etc/ | grep Centos

遞迴搜尋檔案
grep -r Centos /etc/
在 /etc/ 下所有檔案中搜尋 Centos
grep -r --include="*.conf" Centos /etc/


grep -r --include="*.py" --exclude="test_*" -o -n -i -E '(aaa|bbb)' ./
```

## 忽略大小寫

- grep -i Centos /etc/test

## 標示行號

- grep -v Centos /etc/test

## 反向匹配

- grep -v Centos /etc/test
- 只顯示出沒有關鍵字的那幾行資料

## 顯示前後幾行

```shell
# 多顯示後一行
grep -A 1 Centos /etc/test

# 多顯示前一行
grep -B 1 Centos /etc/test

# 多顯示前後各一行
grep -C 1 Centos /etc/test
```

## 正規表示法

```shell
# a 開頭
ls | grep "^a"

# b 結尾
ls | grep "b$"

# a 或 b 開頭
ls | grep "^[ab]"

# a 或 b 結尾
ls | grep "[ab]$"
```