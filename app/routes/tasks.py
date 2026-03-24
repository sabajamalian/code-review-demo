from flask import Blueprint, jsonify, request

from app import db
from app.models import Task, TodoList

tasks_bp = Blueprint("tasks", __name__)


def _get_list_or_404(list_id):
    todo_list = db.session.get(TodoList, list_id)
    if not todo_list:
        return None
    return todo_list


@tasks_bp.route("/api/lists/<int:list_id>/tasks", methods=["GET"])
def get_tasks(list_id):
    if not _get_list_or_404(list_id):
        return jsonify({"error": "list not found"}), 404
    tasks = Task.query.filter_by(list_id=list_id).order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@tasks_bp.route("/api/lists/<int:list_id>/tasks", methods=["POST"])
def create_task(list_id):
    if not _get_list_or_404(list_id):
        return jsonify({"error": "list not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        list_id=list_id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/api/lists/<int:list_id>/tasks/<int:task_id>", methods=["GET"])
def get_task(list_id, task_id):
    if not _get_list_or_404(list_id):
        return jsonify({"error": "list not found"}), 404
    task = db.session.get(Task, task_id)
    if not task or task.list_id != list_id:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task.to_dict())


@tasks_bp.route("/api/lists/<int:list_id>/tasks/<int:task_id>", methods=["PUT"])
def update_task(list_id, task_id):
    if not _get_list_or_404(list_id):
        return jsonify({"error": "list not found"}), 404
    task = db.session.get(Task, task_id)
    if not task or task.list_id != list_id:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "request body is required"}), 400

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "completed" in data:
        task.completed = bool(data["completed"])

    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.route("/api/lists/<int:list_id>/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(list_id, task_id):
    if not _get_list_or_404(list_id):
        return jsonify({"error": "list not found"}), 404
    task = db.session.get(Task, task_id)
    if not task or task.list_id != list_id:
        return jsonify({"error": "task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "task deleted"})
