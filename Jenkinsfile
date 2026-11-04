pipeline {
    agent { label 'dragon' }
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    environment {
        COMPOSE_PROJECT_NAME = 'devops-notes'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps { sh 'docker compose -f compose.yaml build' }
        }
        stage('Run Django Tests') {
            steps { sh 'docker compose -f compose.yaml run --rm --no-deps --entrypoint python web manage.py test' }
        }
        stage('Deploy') {
            steps { sh 'docker compose -f compose.yaml up -d --remove-orphans' }
        }
        stage('Verify Deployment') {
            steps {
                sh '''
                    set -eu
                    for attempt in $(seq 1 30); do
                        if curl --fail --silent http://127.0.0.1:8000/health/; then
                            echo
                            echo "Application is healthy."
                            exit 0
                        fi
                        echo "Waiting for Django app... ($attempt/30)"
                        sleep 2
                    done
                    docker compose -f compose.yaml logs --tail=100 web
                    exit 1
                '''
            }
        }
    }
    post {
        success { echo 'Deployment completed successfully.' }
        failure {
            echo 'Pipeline failed. Check the stage logs.'
            sh 'docker compose -f compose.yaml ps || true'
        }
    }
}
