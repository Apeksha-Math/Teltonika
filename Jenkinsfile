pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from Git repository
                git 'https://github.com/Apeksha-Math/Teltonika.git'
            }
        }
        
        stage('Build') {
            steps {
                // Example for building the socket server
                sh 'cd server-directory && mvn clean package'
            }
        }
        
        stage('Test') {
            steps {
                // Example for testing the socket server
                sh 'cd server-directory && mvn test'
            }
        }
        
        stage('Deploy') {
            steps {
                // Example deployment steps (optional)
                // You can define deployment steps based on your environment and strategy
                echo 'Deploying...'
            }
        }
    }
    
    post {
        success {
            // Actions to perform on successful pipeline run
            echo 'Pipeline succeeded!'
        }
        failure {
            // Actions to perform on failed pipeline run
            echo 'Pipeline failed!'
        }
    }
}
