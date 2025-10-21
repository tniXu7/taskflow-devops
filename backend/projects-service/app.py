from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# Временное хранилище проектов
projects = []

@app.route('/projects', methods=['POST'])
def create_project():
    """Создание нового проекта"""
    data = request.get_json()
    
    # Проверка аутентификации
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization required'}), 401
    
    project = {
        'id': len(projects) + 1,
        'name': data.get('name'),
        'description': data.get('description', ''),
        'created_at': datetime.now().isoformat(),
        'status': 'active',
        'owner': 'current_user'  # В реальном приложении из токена
    }
    
    projects.append(project)
    return jsonify(project), 201

@app.route('/projects', methods=['GET'])
def get_projects():
    """Получение списка проектов"""
    return jsonify({
        'projects': projects,
        'total': len(projects)
    })

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Получение проекта по ID"""
    project = next((p for p in projects if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/projects/<int:project_id>/tasks', methods=['POST'])
def create_task(project_id):
    """Создание задачи в проекте"""
    data = request.get_json()
    
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    if 'tasks' not in project:
        project['tasks'] = []
    
    task = {
        'id': len(project['tasks']) + 1,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'status': 'todo',
        'created_at': datetime.now().isoformat()
    }
    
    project['tasks'].append(task)
    return jsonify(task), 201

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'healthy', 'service': 'projects-service'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)