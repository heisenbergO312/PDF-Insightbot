pipeline {
    agent any

    environment {
        PYTHON_ENV = './venv'  // Path to your virtual environment
        PYTHON_VERSION = '3.9'
        PROJECT_DIR = './backend'  // Path to your backend folder
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    // Ensure Python 3.9+ is installed
                    sh "python3 --version"
                    sh "python3 -m venv ${env.PYTHON_ENV}"  // Create virtual environment
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install dependencies
                    sh ". ${env.PYTHON_ENV}/bin/activate && ${env.PYTHON_ENV}/bin/pip install -r ${env.PROJECT_DIR}/requirements.txt"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    env.PYTHONPATH = "${env.WORKSPACE}/backend"
                }
                sh ". ${env.PYTHON_ENV}/bin/activate && PYTHONPATH=${env.WORKSPACE} pytest ${env.PROJECT_DIR}/tests/tests_backend.py"
            }
        }

        stage('Install Frontend Dependencies') {
            steps {
                script {
                    echo 'Frontend dependencies installation (if any)'
                }
            }
        }

        stage('Frontend Build') {
            steps {
                script {
                    echo 'Frontend build (if any)'
                }
            }
        }

        stage('Package and Archive') {
            steps {
                script {
                    echo 'Package and archive the build'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo 'Clean up after the build'
                }
            }
        }

        stage('Post Actions') {
            steps {
                script {
                    echo 'Build completed'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace'
        }

        success {
            echo 'Build and tests passed successfully!'
        }

        failure {
            echo 'Build or tests failed!'
        }
    }
}
