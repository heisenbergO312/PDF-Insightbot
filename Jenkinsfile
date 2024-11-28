pipeline {
    agent any

    environment {
        // Set environment variables for Python and required tools
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
                    sh "${env.PYTHON_ENV}/bin/pip install -r ${env.PROJECT_DIR}/requirements.txt"  // Install dependencies
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    env.PYTHONPATH = "${env.WORKSPACE}/backend"
                }
                sh 'pytest backend/tests/tests_backend.py'
            }
        }


        stage('Install Frontend Dependencies') {
            steps {
                script {
                    // Frontend installation, skipped if you don't have this stage
                    echo 'Frontend dependencies installation (if any)'
                }
            }
        }

        stage('Frontend Build') {
            steps {
                script {
                    // Frontend build, skipped if not required
                    echo 'Frontend build (if any)'
                }
            }
        }

        stage('Package and Archive') {
            steps {
                script {
                    // Package and archive artifacts, skipped if not required
                    echo 'Package and archive the build'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Clean up any temporary files
                    echo 'Clean up after the build'
                }
            }
        }

        stage('Post Actions') {
            steps {
                script {
                    // Actions after all stages complete
                    echo 'Build completed'
                }
            }
        }
    }

    post {
        always {
            // Clean up actions after the pipeline finishes
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
