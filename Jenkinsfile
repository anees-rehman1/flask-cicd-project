pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-cicd-app'
        DOCKER_TAG = "${env.BUILD_ID}"
        DOCKER_REGISTRY = 'your-docker-registry' // Change this
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/yourusername/flask-cicd-project.git' // Change this
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    sh 'python --version'
                    sh 'pip --version'
                    sh 'pip install -r requirements.txt'
                }
                echo '✅ Python environment setup complete'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest tests/ --verbose --junitxml=test-results.xml'
                }
                echo '✅ Tests completed successfully'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh 'pip install bandit'
                    sh 'bandit -r app/ -f json -o security-report.json || true'
                }
                echo '🔒 Security scan completed'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                }
                echo '🐳 Docker image built successfully'
            }
        }
        
        stage('Test Docker Container') {
            steps {
                script {
                    sh "docker run -d -p 5001:5000 --name test-container ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sleep 10
                    sh 'curl -f http://localhost:5001/api/health || exit 1'
                    sh 'docker stop test-container && docker rm test-container'
                }
                echo '✅ Docker container test passed'
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Uncomment and configure your Docker registry
                    // sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                    // sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest"
                    echo '📦 Image ready for deployment'
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo '🚀 Deploying application...'
                    // Add your deployment commands here
                    // Example: kubectl apply, docker-compose up, etc.
                    echo '✅ Deployment completed'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
            cleanWs()
        }
        success {
            echo '🎉 Pipeline succeeded!'
            // Add notification (Slack, email, etc.)
        }
        failure {
            echo '❌ Pipeline failed!'
            // Add notification (Slack, email, etc.)
        }
    }
}