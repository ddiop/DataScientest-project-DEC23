pipeline {
    agent any
    environment {
        DOCKER_ID = "ddiopegen"
        DOCKER_IMAGE = "datascientestapi"
        DOCKER_TAG = "v.${BUILD_ID}.0"
    }
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
                sh '''
                . venv/bin/activate
                python -m unittest discover -s tests
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
