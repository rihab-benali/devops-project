
from sqlalchemy import inspect  # Add this import at the top
from .auth import role_required
from flask import Blueprint, request, jsonify
from .models import User, Role
from . import db
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt, datetime
from flask import current_app

bp = Blueprint("user", __name__)


@bp.route('/check-tables', methods=['GET'])
def check_tables():
    try:
        # Get database inspector
        inspector = inspect(db.engine)
        
        # Get table names
        tables = inspector.get_table_names()
        
        # Return success response
        return jsonify({
            'status': 'success',
            'tables': tables,
            'count': len(tables)
        }), 200
        
    except Exception as e:
        # Return error response
        return jsonify({
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__
        }), 500

@bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        # Get all users
        users = User.query.all()
        
        # Format the response
        users_data = [{
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role.name if user.role else None
        } for user in users]
        
        return jsonify({
            'status': 'success',
            'count': len(users_data),
            'users': users_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

'''@bp.route("/users", methods=["GET"])
def list_users():
    return jsonify(get_all_users())'''
@bp.route('/')
def index():
    return "Hello from Flask Microservice!"

# This route handles user registration
@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    
    # Default to "user" role if not specified
    role_name = data.get("role", "user")
    
    # Find or create the role (if you want to be extra safe)
    role = Role.query.filter_by(name=role_name).first()
    
    # If role doesn't exist Default to "user" role
    if not role:
        role = Role.query.filter_by(name="user").first()
        if not role:
            return jsonify({"message": "Default user role not found"}), 500
    
    hashed_pw = generate_password_hash(data["password"]).decode("utf-8")
    
    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_pw,
        role=role
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": f"User created with role: {role.name}"})

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        token = jwt.encode({
    "user_id": user.id,
    "role": user.role.name,
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
}, current_app.config["SECRET_KEY"], algorithm="HS256")


        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401




@bp.route("/admin-only", methods=["GET"])
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome, Admin!"})

