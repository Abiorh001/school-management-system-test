pipeline {
    agent {
        kubernetes {
            inheritFrom 'kube-agent'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: jenkins
spec:
  containers:
    - name: python
      image: python:3.12
      command:
        - cat
      tty: true
    - name: sonar-scanner
      image: sonarsource/sonar-scanner-cli:11.1.1.1661_6.2.1
      command:
        - cat
      tty: true
"""
        }
    }
    environment {
        SONAR_HOST_URL = 'http://192.168.1.185:30942'
        SONAR_PROJECT_KEY = 'school_management_system'
    }
    stages {
        stage('Install Python Dependencies') {
            steps {
                container('python') {
                    sh '''
                    echo "Installing Python dependencies..."
                    # Uncomment below and modify as needed
                    # pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Code Analysis') {
            steps {
                container('sonar-scanner') {
                    withCredentials([string(credentialsId: 'SonarQube', variable: 'SONAR_TOKEN')]) {
                        sh '''
                        echo "Starting Code Analysis..."
                        sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.python.version=3.12 \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_TOKEN}
                        '''
                    }
                }
            }
        }

        // stage('Quality Gate Check') {
        //     steps {
        //         container('sonar-scanner') {
        //             withCredentials([string(credentialsId: 'SonarQube', variable: 'SONAR_TOKEN')]) {
        //                 script {
        //                     sh '''
        //                     echo "Setting up jq..."
        //                     mkdir -p ${HOME}/bin
        //                     curl -L https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -o ${HOME}/bin/jq
        //                     chmod +x ${HOME}/bin/jq
        //                     export PATH=${HOME}/bin:$PATH
        //                     jq --version
        //                     '''

        //                     echo "Checking Quality Gate status..."
        //                     def response = sh(
        //                         script: """
        //                             curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${SONAR_PROJECT_KEY}"
        //                         """,
        //                         returnStdout: true
        //                     ).trim()

        //                     // Debug response
        //                     echo "SonarQube Response: ${response}"

        //                     def status = sh(
        //                         script: """
        //                             export PATH=/tmp/bin:$PATH
        //                             echo '${response}' | /tmp/bin/jq -r '.projectStatus.status'
        //                         """,
        //                         returnStdout: true
        //                     ).trim()

        //                     def conditions = sh(
        //                         script: """
        //                             export PATH=/tmp/bin:$PATH
        //                             echo '${response}' | /tmp/bin/jq -r '.projectStatus.conditions'
        //                         """,
        //                         returnStdout: true
        //                     ).trim()

        //                     echo "Quality Gate Conditions: ${conditions}"

        //                     if (status != 'OK') {
        //                         error "Quality Gate failed with status: ${status}. Conditions: ${conditions}"
        //                     } else {
        //                         echo "Quality Gate passed!"
        //                     }
        //                 }
        //             }
        //         }
        //     }
        // }

        stage('Build and Push Docker Image') {
            environment {
                DOCKER_IMAGE = "abiorh/school_management_system:${BUILD_NUMBER}"
            }
            container('python') {
            steps {
                script {
                    sh '''
                    echo "Building Docker Image..."
                    apt-get update && apt-get install -y docker.io
                    docker build -t ${DOCKER_IMAGE} .
                    '''

                    def dockerImage = docker.image("${DOCKER_IMAGE}")
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
                        dockerImage.push()
                    }
                }
            }
        }
    }
    }
}
