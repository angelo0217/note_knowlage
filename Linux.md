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
-- 4 讀
-- 2 寫
-- 1 執行
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
```
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
```sh
centOs 突發cpu暴漲問題
https://blog.csdn.net/weixin_43380635/article/details/91457330
```
# centOs7 關閉update
```
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