from flask import Blueprint, jsonify, request

from app import db
from app.models import TodoList

lists_bp = Blueprint("lists", __name__)


@lists_bp.route("/api/lists", methods=["GET"])
def get_lists():
    lists = TodoList.query.order_by(TodoList.created_at.desc()).all()
    return jsonify([l.to_dict() for l in lists])


@lists_bp.route("/api/lists", methods=["POST"])
def create_list():
    data = request.get_json(silent=True)
    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    todo_list = TodoList(name=data["name"])
    db.session.add(todo_list)
    db.session.commit()
    return jsonify(todo_list.to_dict()), 201


@lists_bp.route("/api/lists/<int:list_id>", methods=["GET"])
def get_list(list_id):
    todo_list = db.session.get(TodoList, list_id)
    if not todo_list:
        return jsonify({"error": "list not found"}), 404
    return jsonify(todo_list.to_dict())


@lists_bp.route("/api/lists/<int:list_id>", methods=["PUT"])
def update_list(list_id):
    todo_list = db.session.get(TodoList, list_id)
    if not todo_list:
        return jsonify({"error": "list not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    todo_list.name = data["name"]
    db.session.commit()
    return jsonify(todo_list.to_dict())


@lists_bp.route("/api/lists/<int:list_id>", methods=["DELETE"])
def delete_list(list_id):
    todo_list = db.session.get(TodoList, list_id)
    if not todo_list:
        return jsonify({"error": "list not found"}), 404

    db.session.delete(todo_list)
    db.session.commit()
    return jsonify({"message": "list deleted"})
