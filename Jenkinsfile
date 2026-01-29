pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'shadow1234090/ci-cd-pipeline'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        // Docker Hub credentials - set these in Jenkins
        DOCKER_REGISTRY_CREDENTIALS = 'docker-hub-credentials'
        VENV_PATH = "${WORKSPACE}/venv"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/anees-rehman1/flask-cicd-project.git' // Update with your repo
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    sh '''
                        echo "=== System Information ==="
                        uname -a
                        echo "Python: $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo 'Not found')"
                        echo "Docker: $(docker --version 2>/dev/null || echo 'Not found')"
                        
                        # Create virtual environment
                        python3 -m venv "${VENV_PATH}" || python -m venv "${VENV_PATH}"
                        . "${VENV_PATH}/bin/activate"
                        python -m pip install --upgrade pip
                    '''
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
                    echo '✅ Dependencies installed'
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
                }
                post {
                    always {
                        junit 'test-results.xml'
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                expression { 
                    // Only run if Docker is available
                    sh(script: 'docker --version', returnStatus: true) == 0 
                }
            }
            steps {
                script {
                    sh """
                        echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                        echo "✅ Docker image built"
                        
                        # List images to verify
                        docker images | grep ${DOCKER_IMAGE}
                    """
                }
            }
        }
        
        stage('Test Docker Container') {
            when {
                expression { 
                    sh(script: 'docker --version', returnStatus: true) == 0 
                }
            }
            steps {
                script {
                    sh '''
                        # Clean up any existing container
                        docker stop flask-test-container 2>/dev/null || true
                        docker rm flask-test-container 2>/dev/null || true
                        
                        # Run container
                        docker run -d -p 5001:5000 --name flask-test-container shadow1234090/ci-cd-pipeline:latest
                        
                        # Wait for container to start
                        echo "Waiting for container to start..."
                        sleep 5
                        
                        # Test the container
                        echo "Testing container..."
                        curl -f http://localhost:5001/api/health || \
                        curl -f http://localhost:5001/api/status || \
                        { echo "Container test failed"; exit 1; }
                        
                        echo "✅ Docker container is working!"
                        
                        # Clean up
                        docker stop flask-test-container
                        docker rm flask-test-container
                    '''
                }
            }
        }
        
        stage('Login to Docker Hub') {
            when {
                expression { 
                    sh(script: 'docker --version', returnStatus: true) == 0 
                }
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )]) {
                        sh """
                            echo "Logging into Docker Hub as ${DOCKER_USERNAME}"
                            echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
                        """
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            when {
                expression { 
                    sh(script: 'docker --version', returnStatus: true) == 0 
                }
                branch 'main'
            }
            steps {
                script {
                    sh """
                        echo "Pushing to Docker Hub..."
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        echo "✅ Images pushed to Docker Hub"
                    """
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo '🚀 Deployment Stage'
                    echo 'Configure your deployment here (Kubernetes, Docker Swarm, etc.)'
                    
                    // Example for simple Docker deployment:
                    // sh '''
                    //     docker stop production-app 2>/dev/null || true
                    //     docker rm production-app 2>/dev/null || true
                    //     docker run -d -p 5000:5000 --name production-app shadow1234090/ci-cd-pipeline:latest
                    // '''
                    
                    echo '✅ Deployment completed'
                    echo 'Application URL: http://your-server:5000'
                }
            }
        }
    }
    
    post {
        always {
            echo '=== Pipeline Cleanup ==='
            script {
                // Clean up Docker containers
                sh '''
                    docker stop flask-test-container 2>/dev/null || true
                    docker rm flask-test-container 2>/dev/null || true
                    echo "Cleanup completed"
                '''
            }
            cleanWs()
        }
        success {
            echo '🎉 Pipeline SUCCESS!'
            // Optional: Send success notification
        }
        failure {
            echo '❌ Pipeline FAILED!'
            // Optional: Send failure notification
        }
        unstable {
            echo '⚠️ Pipeline UNSTABLE!'
        }
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
}