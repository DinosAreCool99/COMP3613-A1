from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    get_user,
    get_user_by_username,
    delete_user,
    get_all_levels,
    get_level
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


# To be removed at another time
@user_views.route('/api/users', methods=['POST'])
def create_user_action():
    data = request.json
    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}) , 409
    user = create_user(data['username'], data['password'])
    return jsonify({"message":"User Created"}), 201


@user_views.route('/signup', methods=["POST"])
def signup_action():
    data = request.get_json()
    if not data:
        return jsonify({"message":"Missing request body."}), 400

    if not data['username'] or not data['password']:
        return jsonify({"message":"Missing username or password parameter."}), 400

    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}), 409

    new_user = create_user(data['username'], data['password'])
    if not new_user:
        return jsonify({"message":"Failed to create."}), 400
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


@user_views.route('/api/users', methods=['DELETE'])
def delete_user_action():
    id = request.args.get('id')
    if not id:
        return jsonify({"message":"Missing id parameter"}), 400

    user = get_user(id)
    if user:
        delete_user(id)
        return jsonify({"message":"User Deleted"}), 200
    return jsonify({"message":"User Not Found"}), 404


#To be implemented
@user_views.route('/api/users/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}"}), 200


@user_views.route('/api/users/level', methods=['GET'])
def get_level_action():
    id = request.args.get('id')
    if not id:
        levels = get_all_levels()
        return jsonify(levels), 200

    user = get_user(id)
    if user:
        level = get_level(user.id)
        return jsonify({"level":f"{level}"}), 200
    return jsonify({"message":"User Not Found"}), 404
