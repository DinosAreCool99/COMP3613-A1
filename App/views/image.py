from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_image, 
    get_all_images,
    get_all_images_json,
    get_images_by_userid_json,
    get_image,
    get_image_json,
    delete_image,
    get_user
)

image_views = Blueprint('image_views', __name__, template_folder='../templates')

@image_views.route('/images', methods=['GET'])
def get_image_page():
    images = get_all_images()
    return render_template('images.html', images=images)


@image_views.route('/api/images', methods=['POST'])
@jwt_required()
def create_image_action():
    data = request.json
    if not data:
        return "Missing request body.", 400

    userId = data['userId']
    if not userId:
        return "Missing userId parameter.", 400

    user = get_user(userId)
    if user:
        #Need to check if user has less than 5 images. Could be controller that takes userID and circumvents the check for the user
        image = create_image(userId)
        return jsonify({"message":"Image created"}), 201
    return jsonify({"message":"User does not exist"}), 404 


@image_views.route('/api/images', methods=['GET'])
def get_images_action():
    args = request.args
    if not args:
        images = get_all_images_json()
        return jsonify(images), 200

    id = args.get('id')
    userId = args.get('userid')
    if id:
        image = get_image_json(id)
        if image:
            return jsonify(image), 200
        return jsonify({"message":"Image does not exist"}), 404 
    if userId:
        if get_user(userId):
            images = get_images_by_userid_json(userId)
            return jsonify(images), 200
        return jsonify({"message":"User does not exist"}), 404 
    return jsonify({"message":"Invalid argument"}), 400


@image_views.route('/api/images', methods=['DELETE'])
@jwt_required()
def delete_image_action():
    id = request.args.get('id')
    if not id:
        return jsonify({"message":"Invalid arguments"}), 400
    if get_image(id):
        delete_image(id)
        return jsonify({"message":"Image Deleted"}), 200
    return jsonify({"message":"Image Not Found"}), 404