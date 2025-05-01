from flask import Blueprint, request, jsonify
from .models import Room, db
from app.kafka_producer import send_event


bp = Blueprint('routes', __name__)

@bp.route('/rooms', methods=['GET'])
def get_all_rooms():
    rooms = Room.query.all()
    return jsonify([{
        "id": room.id,
        "name": room.name,
        "capacity": room.capacity,
        "description": room.description
    } for room in rooms]), 200


@bp.route('/admin/rooms', methods=['POST'])
def create_room():
  

    data = request.get_json()
    new_room = Room(
        name=data.get('name'),
        capacity=data.get('capacity'),
        description=data.get('description'),
        location = data.get('location')
    )
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created", "room_id": new_room.id}), 201


@bp.route('/admin/rooms/<int:id>', methods=['PUT'])
def modify_room(id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    room = Room.query.get_or_404(id)
    data = request.get_json()
    
    room.name = data.get('name', room.name)
    room.capacity = data.get('capacity', room.capacity)
    room.description = data.get('description', room.description)

    db.session.commit()

    return jsonify({"message": "Room updated"}), 200


@bp.route('/admin/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Room deleted"}), 200
