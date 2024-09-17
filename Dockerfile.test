pipeline {
    agent any
    environment {

    }
    stages {
        stage('Install Python venv') {
            steps {
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
                sh '''
                . venv/bin/activate
                python -m unittest discover
                '''
            }
        }
        stage('Deploying') {
            steps {
                script {
                    sh '''

                    '''
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
                input message: "Proceed to push to main ? ", ok: "Yes"
            }
        }
    }
}
