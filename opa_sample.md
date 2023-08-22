# [OPA](https://www.openpolicyagent.org/docs/latest/docker-authorization/#1-create-an-empty-policy-definition-that-will-allow-all-requests)
## 以下實作[參考](https://blog.wu-boy.com/2021/05/comunicate-with-open-policy-agent-using-resful-api/)
### docker 啟動
```shell
sudo docker run -p 8181:8181 openpolicyagent/opa:0.55.0 run --server --log-level debug
```
### data.json
```json
{
  "group_roles": {
    "admin": ["admin"],
    "quality_head_design": ["quality_head_design"],
    "quality_head_system": ["quality_head_system"],
    "quality_head_manufacture": ["quality_head_manufacture"],
    "kpi_editor_design": ["kpi_editor_design"],
    "kpi_editor_system": ["kpi_editor_system"],
    "kpi_editor_manufacture": ["kpi_editor_manufacture"],
    "viewer": ["viewer"],
    "viewer_limit_ds": ["viewer_limit_ds"],
    "viewer_limit_m": ["viewer_limit_m"],
    "design_group_kpi_editor": ["kpi_editor_design", "viewer_limit_ds"],
    "system_group_kpi_editor": ["kpi_editor_system", "viewer_limit_ds"],
    "manufacture_group_kpi_editor": ["kpi_editor_manufacture", "viewer"],
    "project_leader": ["viewer_limit_ds", "viewer_limit_m"]
  },
  "role_permissions": {
    "admin": [
      {"action": "view_all", "object": "design"},
      {"action": "edit", "object": "design"},
      {"action": "view_all", "object": "system"},
      {"action": "edit", "object": "system"},
      {"action": "view_all", "object": "manufacture"},
      {"action": "edit", "object": "manufacture"}
    ],
    "quality_head_design": [
      {"action": "view_all", "object": "design"},
      {"action": "edit", "object": "design"},
      {"action": "view_all", "object": "system"},
      {"action": "view_all", "object": "manufacture"}
    ],
    "quality_head_system": [
      {"action": "view_all", "object": "design"},
      {"action": "view_all", "object": "system"},
      {"action": "edit", "object": "system"},
      {"action": "view_all", "object": "manufacture"}
    ],
    "quality_head_manufacture": [
      {"action": "view_all", "object": "design"},
      {"action": "view_all", "object": "system"},
      {"action": "view_all", "object": "manufacture"},
      {"action": "edit", "object": "manufacture"}
    ],
    "kpi_editor_design": [
      {"action": "view_all", "object": "design"},
      {"action": "edit", "object": "design"}
    ],
    "kpi_editor_system": [
      {"action": "view_all", "object": "system"},
      {"action": "edit", "object": "system"}
    ],
    "kpi_editor_manufacture": [
      {"action": "view_all", "object": "manufacture"},
      {"action": "edit", "object": "manufacture"}
    ],
    "viewer": [
      {"action": "view_all", "object": "design"},
      {"action": "view_all", "object": "system"},
      {"action": "view_all", "object": "manufacture"}
    ],
    "viewer_limit_ds": [
      {"action": "view_all", "object": "design"},
      {"action": "view_all", "object": "system"}
    ],
    "viewer_limit_m": [{"action": "view_l3_project", "object": "manufacture"}]
  }, 
  "policy_setting": {
	  "design_group_kpi_editor": ["123", "456"]
  }
}
```
#### upload
```shell
# /data/sample/auth/acl 這個字段，對齊policy.rego 的 import data.sample.auth.acl
curl --request PUT \
  --url http://localhost:8181/v1/data/sample/auth/acl \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: Insomnia/2023.5.3' \
  --data @data.json
```
### policy.rego
```rego
package sample.auth

import data.sample.auth.acl
import input

# logic that implements RBAC.
default allow = false

allow {
	input.method = "POST"

    # lookup the list of roles for the user
    roles := acl.group_roles[input.user[_]]

    # for each role in that list
    r := roles[_]

    # lookup the permissions list for role r
    permissions := acl.role_permissions[r]

    # for each permission
    p := permissions[_]

    # check if the permission granted to r matches the user's request
    p == {"action": input.action, "object": input.object}
}
```
### policy.rego customer response
```rego
package sample.auth
import input.attributes.request.http as http_request
import data.sample.auth.acl
import input

default request_path = ""
request_path = http_request.path

allow = response {
    input.method = "POST"
	# lookup the list of roles for the user
    roles := acl.group_roles[input.user[_]]

    # for each role in that list
    r := roles[_]

    # lookup the permissions list for role r
    permissions := acl.role_permissions[r]

    # for each permission
    p := permissions[_]

    # check if the permission granted to r matches the user's request
    p == {"action": input.action, "object": input.object}
	
	policy := acl.policy_setting[input.user[_]]
	
    response := {
        "allowed": true,
        "headers": {"x-ext-auth-allow": "yes"},
		"body": {"permission": p, "permissions": permissions, "policy_data": policy}
    }
} else = {
    "allowed": false,
    "headers": {"x-ext-auth-allow": "no"},
    "body": {
      "message": "Unauthorized Request",
      "path": request_path
    },
    "http_status": 301
}
```
#### upload
```shell
# 其中 rbac.authz 這個字段，對齊policy.rego 的 package
curl --request PUT \
  --url http://localhost:8181/v1/policies/sample.auth \
  --header 'Content-Type: application/octet-stream' \
  --header 'User-Agent: Insomnia/2023.5.5' \
  --data @policy.rego
```
### validate
```shell
# /data/sample/auth/allow 這個字段，對齊policy.rego 的 import data.sample.auth.acl 忽略最後一節
curl --request POST \
  --url http://localhost:8181/v1/data/sample/auth/allow \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: Insomnia/2023.5.5' \
  --data '{
  "input": {
    "user": ["design_group_kpi_editor"],
    "action": "edit",
    "object": "design",
	"method": "POST"
  }
}'
```

## [OPA API](https://www.openpolicyagent.org/docs/latest/rest-api/)
### get policies
```shell
curl --request GET \
  --url http://localhost:8181/v1/policies \
  --header 'User-Agent: Insomnia/2023.5.5'
```
### get policy
```shell
curl --request GET \
  --url http://localhost:8181/v1/policies \
  --header 'User-Agent: Insomnia/2023.5.5'
```
### get setting data
```shell
curl --request GET \
  --url http://localhost:8181/v1/data/sample/auth/acl \
  --header 'User-Agent: Insomnia/2023.5.5'
```