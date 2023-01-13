# [參考](https://github.com/swagger-api/swagger-codegen)

## 指令
```shell
program_language=java
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli-v3:3.0.36 generate \
    -i https://petstore.swagger.io/v2/swagger.json \
    -l $program_language \
    -o /local/out/$program_language
```