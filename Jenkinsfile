pipeline {
    agent any

    parameters {
        string(name: 'GIT_REPO', defaultValue: 'https://github.com/EnotShow/Job_parser', description: 'Git repository to clone')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to use')
        string(name: 'DOCKER_COMPOSE_FILE', defaultValue: 'docker-compose.yml', description: 'Docker Compose file to use')
        string(name: 'FOLDER_PATH', defaultValue: '/Projects/Job_parser', description: 'Path to repository folder on local machine')
    }

    stages {
        stage('Fetch Origin') {
            steps {
                script {
                    if (fileExists(params.FOLDER_PATH)) {
                        echo "Repository exists, pulling the latest changes"
                        dir(params.FOLDER_PATH) {
                            sh "git fetch --all"
                            sh "git checkout ${params.GIT_BRANCH}"
                            sh "git pull origin ${params.GIT_BRANCH}"
                        }
                    } else {
                        echo "Cloning the repository from ${params.GIT_REPO}"
                        sh "git clone -b ${params.GIT_BRANCH} ${params.GIT_REPO} ${params.FOLDER_PATH}"
                    }
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                echo "Running Docker Compose using ${params.DOCKER_COMPOSE_FILE}"
                dir(params.FOLDER_PATH) {
                    sh "sudo docker compose -f ${params.DOCKER_COMPOSE_FILE} up --build -d"
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed! Cleaning up Docker containers..."
            dir(params.FOLDER_PATH) {
                sh "docker-compose -f ${params.DOCKER_COMPOSE_FILE} down"
            }
        }

        success {
            echo "Build succeeded! Leaving Docker containers running."
        }
    }
}
