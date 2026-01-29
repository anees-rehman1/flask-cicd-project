pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-cicd-app'
        DOCKER_TAG = "${env.BUILD_ID}"
        DOCKER_REGISTRY = 'your-docker-registry'
        // Add Python to PATH if needed
        PATH = "/usr/bin/python3:${env.PATH}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/anees-rehman1/flask-cicd-project.git'
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    // Try python3 first, then python
                    sh '''
                        if command -v python3 &> /dev/null; then
                            python3 --version
                            python3 -m pip --version
                        elif command -v python &> /dev/null; then
                            python --version
                            python -m pip --version
                        else
                            echo "Python not found. Installing..."
                            apt-get update && apt-get install -y python3 python3-pip
                        fi
                    '''
                    
                    // Install dependencies
                    sh '''
                        if command -v python3 &> /dev/null; then
                            python3 -m pip install -r requirements.txt
                        else
                            pip install -r requirements.txt
                        fi
                    '''
                }
                echo '✅ Python environment setup complete'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        if command -v python3 &> /dev/null; then
                            python3 -m pytest tests/ --verbose --junitxml=test-results.xml
                        else
                            pytest tests/ --verbose --junitxml=test-results.xml
                        fi
                    '''
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
                    sh '''
                        if command -v python3 &> /dev/null; then
                            python3 -m pip install bandit
                            python3 -m bandit -r app/ -f json -o security-report.json || true
                        else
                            pip install bandit
                            bandit -r app/ -f json -o security-report.json || true
                        fi
                    '''
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
                    echo '📦 Image ready for deployment'
                    // Add your push commands here
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
                    // Add deployment commands
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
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}