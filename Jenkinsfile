pipeline {
    agent any
    stages {
        stage('Install Python venv') {
            steps {
                sh '''
                which pg_config || echo "pg_config not found"
                '''
                sh 'sudo apt update && sudo apt install -y python3-venv'
            }
        }
        stage('Building') {
            steps {
                script {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Testing') {
            steps {
                script {
                    sh '''
                    . venv/bin/activate
                    pytest --maxfail=1 --disable-warnings
                    '''
                }
            }
        }
        stage('Deploying') {
            steps {
                script {
                    try {
                        sh '''
                        docker-compose up --build
                        '''
                    } catch (Exception e) {
                        echo "Deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                sh 'docker system prune -af'
            }
        }
        stage('User Acceptance') {
            steps {
                input message: "Proceed to push to main ?", ok: "Yes"
            }
        }
    }
}
