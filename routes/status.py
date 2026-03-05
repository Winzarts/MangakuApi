from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)

@status_bp.route("/", methods=["GET"])
def get_status():
    return jsonify({
        "message": "API is running",
        "status": "Online",
        "Response": "200"
    })