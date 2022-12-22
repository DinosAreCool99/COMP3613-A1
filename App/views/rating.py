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
    if get_user(data['creatorId']) and get_user(data['targetId']):
        if data['creatorId'] != data['targetId']:
            
            prev = get_rating_by_actors(data['creatorId'], data['targetId'])
            if prev:
                return jsonify({"message":"Current user already rated this user"}) 
            rating = create_rating(data['creatorId'], data['targetId'], data['score'])
            return jsonify({"message":"Rating created"}) 

        return jsonify({"message":"User cannot rate self"})
    return jsonify({"message":"User not found"}) 

@rating_views.route('/api/ratings', methods=['GET'])
def get_ratings_action():
    args = request.args
    if not args:
        ratings = get_all_ratings_json()
        return jsonify(ratings)
    id = args.get('id')
    creatorid = args.get('creatorid')
    targetid = args.get('targetid')
    if id:
        rating = get_rating(id)
        if rating:
            return rating.toJSON()
        return jsonify({"message":"Rating not found"})
    if creatorid:
        if get_user(creatorid):
            ratings = get_ratings_by_creator(creatorid)
            if ratings:
                return jsonify(ratings) 
            return jsonify({"message":"No ratings by this user found"})
        return jsonify({"message":"User not found"})
    if targetid:
        if get_user(targetid):
            rating = get_ratings_by_target(targetid)
            if rating:
                return jsonify(rating) 
            return jsonify({"message":"No ratings for this user found"})
        return jsonify({"message":"User not found"})
    return jsonify({"message":"Invalid argument"}) 

@rating_views.route('/api/ratings', methods=['PUT'])
def update_rating_action():
    data = request.json
    rating = update_rating(data['id'], data['score'])
    if rating:
        return jsonify({"message":"Rating updated"})
    return jsonify({"message":"Rating not found"})

@rating_views.route('/api/ratings/calc', methods=['GET'])
def get_calculated_rating_action():
    targetId = request.args.get('targetid')
    if get_user(targetId):
        rating = get_calculated_rating(targetId)
        if rating:
            return jsonify({"calculated rating": rating}) 
        return jsonify({"message":"No ratings by this user found"})
    return jsonify({"message":"User not found"})

