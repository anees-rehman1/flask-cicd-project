pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DOCKER_IMAGE = 'flask-cicd-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/anees-rehman1/flask-cicd-project.git',
                        credentialsId: 'github-token'
                    ]]
                ])
                echo '✅ Code checked out successfully'
            }
        }
        
        stage('Verify Environment') {
            steps {
                sh '''
                    echo "=== Python Environment ==="
                    python --version
                    pip --version
                    echo "=== Directory ==="
                    ls -la
                    echo "=== Requirements ==="
                    cat requirements.txt
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing Python dependencies..."
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    echo "Dependencies installed!"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running tests..."
                    python -m pytest tests/ -v --junitxml=test-results.xml
                    echo "Tests completed!"
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Installing Docker..."
                    apt-get update && apt-get install -y docker.io
                    echo "Building Docker image..."
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    echo "Docker images:"
                    docker images | grep flask
                '''
            }
        }
        
        stage('Test Container') {
            steps {
                sh '''
                    echo "Testing Docker container..."
                    docker run -d -p 5000:5000 --name test-app ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 10
                    echo "Testing API..."
                    curl -f http://localhost:5000/api/health || (docker logs test-app && exit 1)
                    echo "API Response:"
                    curl -s http://localhost:5000/api/health | python -m json.tool
                '''
            }
        }
        
        stage('Cleanup & Report') {
            steps {
                sh '''
                    echo "Cleaning up..."
                    docker stop test-app || true
                    docker rm test-app || true
                '''
                echo '🎉 Pipeline completed successfully!'
                echo 'Docker image: flask-cicd-app:latest'
                echo 'Run with: docker run -d -p 5000:5000 flask-cicd-app:latest'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finished'
            sh '''
                docker stop test-app 2>/dev/null || true
                docker rm test-app 2>/dev/null || true
            '''
        }
        success {
            echo '✅ SUCCESS! Flask app is ready!'
            echo 'Visit: http://localhost:5000'
        }
        failure {
            echo '❌ Pipeline failed'
        }
    }
}