# 新增cmd
```shell
將對應的檔案如sqlite, mysql等放置同一個資料
env path，新增該路徑
```
# 客製shell, note.bat
## cmd 執行 note.bat，就會開啟對應服務
```shell
@ECHO OFF
start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Notepad++"
```
#mysql
```shell
https://dev.mysql.com/downloads/mysql/
下載 Windows (x86, 64-bit), ZIP Archive 解壓縮
path add
D:\mysql-8.0.29-winx64\bin
```
# sqlite
```shell
https://www.sqlite.org/download.html
下載
Precompiled Binaries for Windows
  sqlite-dll-win64-x64-3400100.zip
  sqlite-tools-win32-x86-3400100.zip
解壓縮放置路徑，添加至path
```