from flask import Blueprint, request, jsonify
from . import db
from .models import Reservation
import requests
from datetime import datetime
import os
from app.kafka_producer import send_event

reservation_bp = Blueprint('reservation', __name__)

ROOM_SERVICE_URL = os.getenv("ROOM_SERVICE_URL", "http://room_service:5001")

@reservation_bp.route("/rooms", methods=["GET"])
def get_all_rooms():
    res = requests.get(f"{ROOM_SERVICE_URL}/rooms")
    return jsonify(res.json()), res.status_code

@reservation_bp.route("/rooms/available", methods=["GET"])
def get_available_rooms():
    start = request.args.get("start_date")
    end = request.args.get("end_date")

    res = requests.get(f"{ROOM_SERVICE_URL}/rooms")
    rooms = res.json()

    available = []
    for room in rooms:
        reservations = Reservation.query.filter_by(room_id=room["id"]).all()
        if all(r.end_date < datetime.strptime(start, "%Y-%m-%d").date() or r.start_date > datetime.strptime(end, "%Y-%m-%d").date() for r in reservations):
            available.append(room)

    return jsonify(available)

@reservation_bp.route("/reservations", methods=["POST"])
def reserve():
    data = request.json
    r = Reservation(
        user_id=data["user_id"],
        room_id=data["room_id"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"id": r.id, "status": r.status})

@reservation_bp.route("/reservations/<int:id>", methods=["GET"])
def get_reservation(id):
    r = Reservation.query.get(id)
    if not r:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": r.id,
        "room_id": r.room_id,
        "status": r.status,
        "start_date": r.start_date,
        "end_date": r.end_date
    })

# Admin endpoints
@reservation_bp.route("/reservations/<int:id>", methods=["PUT"])
def update_reservation_status(id):
    data = request.json
    r = Reservation.query.get(id)
    if not r:
        return jsonify({"error": "Not found"}), 404
    r.status = data["status"]
    db.session.commit()
    return jsonify({"status": r.status})
