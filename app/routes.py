from flask import Blueprint, render_template, jsonify
import os
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/status')
def status():
    return jsonify({
        'status': 'success',
        'message': 'Flask CI/CD Pipeline is working!',
        'timestamp': datetime.now().isoformat(),
        'environment': os.getenv('FLASK_ENV', 'development'),
        'debug_mode': os.getenv('DEBUG', 'False')
    })

@main_bp.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'flask-cicd-app',
        'timestamp': datetime.now().isoformat()
    })

@main_bp.route('/api/info')
def info():
    return jsonify({
        'app': 'Flask CI/CD Demo',
        'version': '1.0.0',
        'author': 'Your Name',
        'description': 'A demo Flask app with complete CI/CD pipeline',
        'features': ['Dockerized', 'Jenkins Pipeline', 'Automated Testing', 'CI/CD']
    })