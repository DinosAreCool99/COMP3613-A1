from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    get_user,
    get_user_by_username,
    update_user,
    delete_user,
    login_user,
    logout_user,
    get_level,
    authenticate
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')


@user_views.route('/api/users', methods=['POST'])
def create_user_action():
    data = request.json
    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}) , 400
    user = create_user(data['username'], data['password'])
    return jsonify({"message":"User Created"}), 201


@user_views.route('/signup', methods=["POST"])
def signup_action():
    data = request.get_json()
    if not data:
        return "Missing request body.", 400

    username = data['username']
    password = data['password']
    if not username or not password:
        return "Missing username or password parameter.", 400

    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}), 400

    new_user = create_user(username, password)
    if not new_user:
        return "Failed to create.", 400
    return new_user.toJSON(), 201


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    id = request.args.get('id')
    if not id:
        users = get_all_users_json()
        return jsonify(users), 200
    user = get_user(id)
    if user:
        return user.toJSON(), 200
    return jsonify({"message":"User Not Found"}), 404


@user_views.route('/api/users', methods=['PUT'])
def update_user_action():
    data = request.json
    if not data:
        return "Missing request body.", 400

    username = data['username']
    id = data['id']
    if not username or not id:
        return "Missing username or id parameter.", 400

    user = update_user(id, username)
    if user:
        return jsonify({"message":"User Updated"}), 200
    return jsonify({"message":"User Not Found"}), 404


@user_views.route('/api/users', methods=['DELETE'])
def delete_user_action():
    id = request.args.get('id')
    if not id:
        return jsonify({"message":"Id Not Valid"}), 400
    user = get_user(id)
    if user:
        delete_user(id)
        return jsonify({"message":"User Deleted"}), 200
    return jsonify({"message":"User Not Found"}), 404


@user_views.route('/api/users/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}"}), 200


@user_views.route('/api/users/level', methods=['GET'])
def get_level_action():
    id = request.args.get('id')
    if not id:
        # To change to return level for all users
        return jsonify({"message":"Not yet implemented"}), 302
    user = get_user(id)
    if user:
        level = get_level(user.id)
        return jsonify({"level":f"{level}"}), 200
    return jsonify({"message":"User Not Found"}), 404
