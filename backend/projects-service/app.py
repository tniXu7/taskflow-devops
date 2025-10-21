Set-Content backend/projects-service/app.py 'from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Временное хранилище проектов (в продакшене будет БД)
projects = []

@app.route("/projects", methods=["POST"])
def create_project():
    """Создание нового проекта"""
    data = request.get_json()
    
    project = {
        "id": len(projects) + 1,
        "name": data.get("name"),
        "description": data.get("description", ""),
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    projects.append(project)
    return jsonify(project), 201

@app.route("/projects", methods=["GET"])
def get_projects():
    """Получение списка проектов"""
    return jsonify(projects)

@app.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Получение проекта по ID"""
    project = next((p for p in projects if p["id"] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({"error": "Project not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)'