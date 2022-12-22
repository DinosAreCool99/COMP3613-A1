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
    user = get_user(data['userId'])
    #Need to check if user has less than 5 images. Could be controller that takes userID and circumvents the check for the user
    if user:
        image = create_image(data['userId'])
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/api/images', methods=['GET'])
def get_images_action():
    args = request.args
    if not args:
        images = get_all_images_json()
        return jsonify(images)
    id = args.get('id')
    userId = args.get('userid')
    if id:
        image = get_image_json(id)
        return jsonify(image)
    if userId:
        images = get_images_by_userid_json(userId)
        return jsonify(images)
    return jsonify({"message":"Invalid argument"})

@image_views.route('/api/images', methods=['DELETE'])
@jwt_required()
def delete_image_action():
    id = request.args.get('id')
    if not id:
        return jsonify({"message":"Invalid arguments"})
    if get_image(id):
        delete_image(id)
        return jsonify({"message":"Image Deleted"}) 
    return jsonify({"message":"Image Not Found"}) 