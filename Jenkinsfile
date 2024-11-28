pipeline {
    agent any

    environment {
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'
        VENV_DIR = 'venv'
        PYTHON_VERSION = '3.9'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Backend Environment') {
            steps {
                dir("${BACKEND_DIR}") {
                    script {
                        sh '''
                        python${PYTHON_VERSION} -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Backend Lint and Test') {
            steps {
                dir("${BACKEND_DIR}") {
                    script {
                        sh '''
                        source ${VENV_DIR}/bin/activate
                        flake8 --max-line-length=88 .
                        pytest --disable-warnings
                        '''
                    }
                }
            }
        }

        stage('Install Frontend Dependencies') {
            steps {
                dir("${FRONTEND_DIR}") {
                    script {
                        sh '''
                        npm install
                        '''
                    }
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir("${FRONTEND_DIR}") {
                    script {
                        sh '''
                        npm run build
                        '''
                    }
                }
            }
        }

        stage('Package and Archive') {
            steps {
                script {
                    sh '''
                    mkdir -p build_package
                    cp -r ${BACKEND_DIR} ${FRONTEND_DIR}/build build_package/
                    '''
                }
                archiveArtifacts artifacts: 'build_package/**', fingerprint: true
            }
        }

        stage('Clean Up') {
            steps {
                cleanWs()
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed.'
        }
    }
}
