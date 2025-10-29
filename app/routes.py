from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import Todo

todos_bp = Blueprint("todos", __name__)


def _current_user_id() -> int:
    return int(get_jwt_identity())


@todos_bp.get("/todos")
@jwt_required()
def list_todos():
    user_id = _current_user_id()
    todos = (
        Todo.query.filter_by(user_id=user_id)
        .order_by(Todo.created_at.desc())
        .all()
    )
    return jsonify([
        {"id": t.id, "title": t.title, "completed": t.completed, "created_at": t.created_at.isoformat()}
        for t in todos
    ])


@todos_bp.post("/todos")
@jwt_required()
def create_todo():
    user_id = _current_user_id()
    payload = request.get_json() or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify({"message": "title is required"}), 400
    todo = Todo(title=title, user_id=user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "completed": todo.completed}), 201


@todos_bp.patch("/todos/<int:todo_id>")
@jwt_required()
def update_todo(todo_id: int):
    user_id = _current_user_id()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({"message": "not found"}), 404
    payload = request.get_json() or {}
    if "title" in payload:
        title = (payload.get("title") or "").strip()
        if not title:
            return jsonify({"message": "title cannot be empty"}), 400
        todo.title = title
    if "completed" in payload:
        todo.completed = bool(payload.get("completed"))
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "completed": todo.completed})


@todos_bp.delete("/todos/<int:todo_id>")
@jwt_required()
def delete_todo(todo_id: int):
    user_id = _current_user_id()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({"message": "not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


