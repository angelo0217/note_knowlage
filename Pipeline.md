# Jenkins Pipeline
## Branch Tag use same field
```shell
@Library('common_lib') _


pipeline {
    environment {
		VERSION = "v1.3.2"
    }
    // agent any
    agent any
    stages {
        stage("Git Checkout") {
            steps {
                script{
                    def scmVars;
                    try{
                        scmVars =  git(
                            url: "https://github.com/Orgin/repo.git",
                            credentialsId: 'github_access_token',
                            branch: "$VERSION"
                        )
                    } catch(err) {
                        echo ">>>>>> to use tag"
                        scmVars = checkout scm: [
                            $class: 'GitSCM', 
                            userRemoteConfigs: [[url: "https://github.com/Orgin/repo.git", credentialsId: "github_access_token"]], 
                            branches: [[name: "refs/tags/$VERSION"]]
                        ], poll: false
                    }
                    
                    echo scmVars.GIT_COMMIT
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            echo ''
        }
    }
}
```
## sub job get executor
```shell
@Library('common_lib') _

pipeline {
    environment {
        TOKEN = ' '
    }

    agent any
    stages {
        stage('Get API Token') {
            steps {
                withCredentials([string(credentialsId: "XXXX", variable: 'SECRET')]) {
                    script {
                        TOKEN = env.SECRET
                    }
                }
            }
        }
        stage('Upload') {
            steps {
                script {
                    wrap([$class: 'BuildUser']) {
                        echo "BUILD_USER_ID: ${BUILD_USER_ID}"
                    }
                }
            }
        }
    }
}

```