pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-cicd-app'
        DOCKER_TAG = "${env.BUILD_ID}"
        // Remove or update this based on your Docker registry
        // DOCKER_REGISTRY = 'your-docker-registry'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // FIXED: Use YOUR GitHub username
                git branch: 'main', 
                    url: 'https://github.com/anees-rehman1/flask-cicd-project.git'
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    sh 'python --version'
                    sh 'pip --version'
                    // Use virtual environment
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
                echo '✅ Python environment setup complete'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh '. venv/bin/activate && pytest tests/ --verbose --junitxml=test-results.xml'
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
                    sh '. venv/bin/activate && pip install bandit || true'
                    sh '. venv/bin/activate && bandit -r app/ -f json -o security-report.json || true'
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
                    sh 'curl -f http://localhost:5001/api/health || (docker logs test-container && exit 1)'
                    sh 'docker stop test-container || true'
                    sh 'docker rm test-container || true'
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
                    echo '📦 Image built successfully'
                    echo 'To push to registry, configure DOCKER_REGISTRY variable'
                    // Uncomment when you have a registry
                    // sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                    // sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo '🚀 Application ready for deployment'
                    echo 'Docker Image: flask-cicd-app:latest'
                    echo 'To deploy: docker run -d -p 5000:5000 flask-cicd-app:latest'
                    // Add your deployment commands here
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            // Clean up Docker containers
            sh 'docker stop test-container || true'
            sh 'docker rm test-container || true'
            cleanWs()
        }
        success {
            echo '🎉 Pipeline succeeded!'
            echo 'Your Flask app is ready at: http://localhost:5000'
            echo 'To run: docker run -d -p 5000:5000 flask-cicd-app:latest'
        }
        failure {
            echo '❌ Pipeline failed!'
            echo 'Check the error messages above'
        }
    }
}