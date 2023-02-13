# Git

## remove tag

### remove remote

```shell
git push origin :refs/tags/v1.0.14
```

### remove local

```shell
git tag -d v1.0.14
```

## reset

```shell
git reset --hard a302437e348729edd98bbe2bd6b5c385db1972d7
git push -f  # 更新遠端
```

## create tag

```shell
git tag -a v2.1.0
git push origin v2.1.0
```

##還原
還原目標在備份倉，執行下面指令
```
git push --mirror {new_repository_path}
```
```shell
#!/bin/bash

cwd=$(pwd)

while read -r line; do

    repo_name=$line

    repo_path=$cwd/remote/$repo_name
    
    mkdir $cwd/src/$repo_name
    cd $cwd/src/$repo_name
    git init
    git remote add origin $repo_path
    git pull origin master || git pull origin main
    cd $cwd

done < <(ls remote)
```
```shell
while read -r line; do
repo_name=$line
echo $repo_name
done < <(ls $line)
```
# check out tags
```shell
git clone xxxx.git
git checkout tags/1.1.1

or
git clone --depth 1 --branch 1.1.1 xxxx.git
```