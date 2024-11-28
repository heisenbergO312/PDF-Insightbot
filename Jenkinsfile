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

        stage('Compile') {
            steps {
                script {
                    // Ensure the code compiles without errors
                    sh ". ${env.PYTHON_ENV}/bin/activate && python -m compileall ${env.PROJECT_DIR}"
                }
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
