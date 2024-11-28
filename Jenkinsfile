pipeline {
    agent any
    environment {
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'
    }
    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }
        
        stage('Set Up Backend Environment') {
            steps {
                dir("${env.BACKEND_DIR}") {
                    script {
                        // Use python3 for version 3.13
                        sh 'python3 -m venv venv'
                    }
                }
            }
        }
        
        stage('Backend Lint and Test') {
            steps {
                dir("${env.BACKEND_DIR}") {
                    script {
                        // Install dependencies and run tests
                        sh './venv/bin/pip install -r requirements.txt'
                        sh './venv/bin/pytest'
                    }
                }
            }
        }
        
        stage('Install Frontend Dependencies') {
            steps {
                dir("${env.FRONTEND_DIR}") {
                    script {
                        // Install frontend dependencies (assuming you're using npm)
                        sh 'npm install'
                    }
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir("${env.FRONTEND_DIR}") {
                    script {
                        // Run frontend build
                        sh 'npm run build'
                    }
                }
            }
        }
        
        stage('Package and Archive') {
            steps {
                // Archive the build artifacts if needed
                archiveArtifacts allowEmptyArchive: true, artifacts: '**/target/*.jar', onlyIfSuccessful: true
            }
        }

        stage('Clean Up') {
            steps {
                // Clean up workspace if necessary
                cleanWs()
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Build successful.'
        }
        failure {
            echo 'Build failed.'
        }
    }
}
