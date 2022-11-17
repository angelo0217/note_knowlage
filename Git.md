# Git
## remove tag
### remove remote
```
git push origin :refs/tags/v1.0.14
```
### remove local
```
git tag -d v1.0.14
```
## reset
```
git reset --hard a302437e348729edd98bbe2bd6b5c385db1972d7
git push -f (更新遠端)
```
## create tag
```
git tag -a v2.1.0
git push origin v2.1.0
```