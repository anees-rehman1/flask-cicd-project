pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-cicd-app'
        DOCKER_TAG = "${env.BUILD_ID}"
        DOCKER_REGISTRY = 'https://hub.docker.com/repository/docker/shadow1234090/ci-cd-pipeline/general' // Change this
        VENV_PATH = "${WORKSPACE}/venv"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/anees-rehman1/flask-cicd-project.git' // Change this
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    // Check Python version
                    sh '''
                        python3 --version || true
                        python --version || true
                    '''
                    
                    // Create virtual environment
                    sh """
                        python3 -m venv "${VENV_PATH}" || python -m venv "${VENV_PATH}"
                        . "${VENV_PATH}/bin/activate"
                        python -m pip install --upgrade pip
                    """
                    
                    echo '✅ Python virtual environment created'
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh """
                        . "${VENV_PATH}/bin/activate"
                        pip install -r requirements.txt
                    """
                    echo '✅ Dependencies installed successfully'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh """
                        . "${VENV_PATH}/bin/activate"
                        pytest tests/ --verbose --junitxml=test-results.xml
                    """
                    echo '✅ Tests completed successfully'
                }
                post {
                    always {
                        junit 'test-results.xml'
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh """
                        . "${VENV_PATH}/bin/activate"
                        pip install bandit
                        bandit -r app/ -f json -o security-report.json || true
                    """
                    echo '🔒 Security scan completed'
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                script {
                    sh """
                        . "${VENV_PATH}/bin/activate"
                        pip install flake8 pylint
                        flake8 app/ --max-line-length=120 --exit-zero
                        pylint app/ --exit-zero || true
                    """
                    echo '📊 Code quality checks completed'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                    echo '🐳 Docker image built successfully'
                }
            }
        }
        
        stage('Test Docker Container') {
            steps {
                script {
                    // Clean up any existing test container
                    sh 'docker stop test-container || true && docker rm test-container || true'
                    
                    // Run container with health check
                    sh "docker run -d -p 5001:5000 --name test-container ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    
                    // Wait for container to be ready
                    sh '''
                        for i in {1..30}; do
                            if docker ps --filter "name=test-container" --filter "health=healthy" | grep -q test-container; then
                                echo "Container is healthy"
                                break
                            fi
                            echo "Waiting for container to be healthy... ($i/30)"
                            sleep 2
                        done
                    '''
                    
                    // Test the API
                    sh 'curl -f http://localhost:5001/api/health || curl -f http://localhost:5001/api/status || exit 1'
                    
                    // Clean up
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
                    // docker.withRegistry('https://registry.example.com', 'credentials-id') {
                    //     sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    //     sh "docker push ${DOCKER_IMAGE}:latest"
                    // }
                    echo '📦 Image ready for deployment'
                    echo 'Note: Configure Docker registry credentials in Jenkins to enable push'
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
                    // Example for Docker Compose deployment:
                    // sh 'docker-compose down && docker-compose up -d'
                    
                    // Example for Kubernetes:
                    // sh 'kubectl apply -f k8s/'
                    
                    echo '✅ Deployment completed'
                    echo 'Application should be available at: http://your-server:5000'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
            // Clean up Docker containers
            sh 'docker stop test-container || true && docker rm test-container || true'
            // Clean up virtual environment (optional)
            // sh "rm -rf ${VENV_PATH}"
            cleanWs()
        }
        success {
            echo '🎉 Pipeline succeeded!'
            // Add notification (Slack, email, etc.)
            // slackSend color: 'good', message: "Pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded!"
        }
        failure {
            echo '❌ Pipeline failed!'
            // Add notification (Slack, email, etc.)
            // slackSend color: 'danger', message: "Pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} failed!"
        }
        unstable {
            echo '⚠️ Pipeline unstable!'
        }
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }
    
    triggers {
        // GitHub webhook trigger
        githubPush()
        
        // Poll SCM every minute (optional backup)
        pollSCM('* * * * *')
    }
}