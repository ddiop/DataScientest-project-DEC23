pipeline {
    agent any
 environment {
        DOCKER_ID = "ddiopegen"
        DOCKER_IMAGE = "australian_api"
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
            // Afficher le chemin de docker-compose pour vérification
            sh 'echo "PATH=$PATH"'
            sh 'which docker-compose || echo "docker-compose non trouvé"'

            try {
                // Assurez-vous que docker-compose est dans le PATH avant d'exécuter
                sh '''
                export PATH=$PATH:/usr/local/bin
                docker rm -f Australian || true
                    docker build -t $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG .
                    docker run -d -p 8000:8000 --name Australian $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG
                '''
            } catch (Exception e) {
                echo "Le déploiement a échoué : ${e.getMessage()}"
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