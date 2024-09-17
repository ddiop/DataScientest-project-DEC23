pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                // Créer un environnement virtuel
                sh 'python3 -m venv venv'

                // Activer l'environnement virtuel
                sh '. venv/bin/activate'

                // Installer les dépendances
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Activer l'environnement virtuel et exécuter les tests
                sh '. venv/bin/activate && venv/bin/pytest --no-header --no-summary -q'
            }
        }
    }

    post {
        always {
            // Collecte des résultats de test
            junit '**/test-results.xml'
        }
    }
}
