from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_rating, 
    get_all_ratings,
    get_all_ratings_json,
    get_rating,
    get_ratings_by_target,
    get_ratings_by_creator,
    get_rating_by_actors,
    update_rating,
    get_user,
    get_calculated_rating
)

rating_views = Blueprint('rating_views', __name__, template_folder='../templates')


@rating_views.route('/api/ratings', methods=['POST'])
@jwt_required()
def create_rating_action():
    data = request.json
    if not data['creatorId'] and not data['targetId']:
        return jsonify({"message":"Missing creatorId or targetId parameter."}), 400

    if get_user(data['creatorId']) and get_user(data['targetId']):
        if data['creatorId'] != data['targetId']:
            previous = get_rating_by_actors(data['creatorId'], data['targetId'])
            if previous:
                return jsonify({"message":"Current user already rated this user"}), 409
            rating = create_rating(data['creatorId'], data['targetId'], data['score'])
            return jsonify({"message":"Rating created"}), 201

        return jsonify({"message":"User cannot rate self"}), 409
    return jsonify({"message":"Creator or Target not found"}), 404


@rating_views.route('/api/ratings', methods=['GET'])
def get_ratings_action():
    args = request.args
    if not args:
        ratings = get_all_ratings_json()
        return jsonify(ratings), 200

    id = args.get('id')
    creatorid = args.get('creatorid')
    targetid = args.get('targetid')
    if id:
        rating = get_rating(id)
        if rating:
            return rating.toJSON(), 200
        return jsonify({"message":"Rating not found"}), 404
    if creatorid:
        if get_user(creatorid):
            ratings = get_ratings_by_creator(creatorid)
            if ratings:
                return jsonify(ratings), 200
            return jsonify({"message":"No ratings by this user found"}), 404
        return jsonify({"message":"User not found"}), 404
    if targetid:
        if get_user(targetid):
            rating = get_ratings_by_target(targetid)
            if rating:
                return jsonify(rating), 200
            return jsonify({"message":"No ratings for this user found"}), 404
        return jsonify({"message":"User not found"}), 404
    return jsonify({"message":"Invalid argument"}), 400


@rating_views.route('/api/ratings', methods=['PUT'])
def update_rating_action():
    data = request.json
    rating = update_rating(data['id'], data['score'])
    if rating:
        return jsonify({"message":"Rating updated"}), 200
    return jsonify({"message":"Rating not found"}), 404


@rating_views.route('/api/ratings/calc', methods=['GET'])
def get_calculated_rating_action():
    targetId = request.args.get('targetid')
    if not targetID:
        return jsonify({"message":"Invalid argument"}), 400
    if get_user(targetId):
        rating = get_calculated_rating(targetId)
        if rating:
            return jsonify({"calculated rating": rating}), 200
        return jsonify({"message":"No ratings by this user found"}), 404
    return jsonify({"message":"User not found"}), 404