pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = 'yourdockerhubusername/flask-cicd-app'  // CHANGE THIS
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        GIT_REPO = 'https://github.com/yourusername/flask-cicd-project.git'  // CHANGE THIS
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: '${GIT_REPO}'
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    sh '''
                        echo "Setting up Python environment..."
                        python3 --version
                        pip3 --version
                        
                        # Create virtual environment
                        python3 -m venv venv || python -m venv venv
                    '''
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        # Activate virtual environment and install dependencies
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        echo "✅ Dependencies installed"
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        echo "Running tests..."
                        pytest tests/ --verbose --junitxml=test-results.xml
                        echo "✅ Tests completed"
                    '''
                }
                post {
                    always {
                        junit 'test-results.xml'
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        echo "Building Docker image..."
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                        echo "✅ Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    '''
                }
            }
        }
        
        stage('Test Docker Container') {
            steps {
                script {
                    sh '''
                        echo "Testing Docker container..."
                        docker run -d -p 5001:5000 --name flask-test-container ${DOCKER_IMAGE}:${DOCKER_TAG}
                        sleep 10
                        
                        # Check if container is running
                        docker ps | grep flask-test-container
                        
                        # Test the API endpoint
                        curl -f http://localhost:5001/api/health || exit 1
                        curl -f http://localhost:5001/api/status || exit 1
                        
                        # Stop and remove test container
                        docker stop flask-test-container
                        docker rm flask-test-container
                        echo "✅ Docker container test passed"
                    '''
                }
            }
        }
        
        stage('Login to Docker Hub') {
            steps {
                script {
                    sh '''
                        echo "Logging into Docker Hub..."
                        echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                        echo "✅ Logged into Docker Hub"
                    '''
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    sh '''
                        echo "Pushing images to Docker Hub..."
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        echo "✅ Images pushed to Docker Hub"
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh '''
                        echo "🚀 Starting deployment..."
                        echo "Deployment would happen here"
                        echo "Example: kubectl apply -f deployment.yaml"
                        echo "Example: docker-compose -f production.yml up -d"
                        echo "✅ Deployment simulation complete"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            sh '''
                echo "Cleaning up..."
                docker stop flask-test-container 2>/dev/null || true
                docker rm flask-test-container 2>/dev/null || true
                echo "Cleanup completed"
            '''
        }
        success {
            echo '🎉 Pipeline succeeded!'
            // Send notification (Slack/Email)
            sh '''
                echo "Sending success notification..."
                # Add your notification commands here
            '''
        }
        failure {
            echo '❌ Pipeline failed!'
            // Send notification (Slack/Email)
            sh '''
                echo "Sending failure notification..."
                # Add your notification commands here
            '''
        }
    }
}