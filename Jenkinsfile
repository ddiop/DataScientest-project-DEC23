pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'PYTHONPATH=. pytest --maxfail=1 --disable-warnings'
            }
        }
    }

    post {
        always {
            junit '**/test-results.xml'  // Collecte des résultats de test, si nécessaire
        }
    }
}
