from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_ranking, 
    get_all_rankings,
    get_all_rankings_json,
    get_ranking,
    get_rankings_by_image,
    get_rankings_by_creator,
    get_ranking_by_actors,
    get_calculated_ranking,
    update_ranking,
    get_user,
    get_image
)

ranking_views = Blueprint('ranking_views', __name__, template_folder='../templates')

@ranking_views.route('/api/rankings', methods=['POST'])
@jwt_required()
def create_ranking_action():
    data = request.json
    if not data['creatorId'] and not data['imageId']:
        return jsonify({"message":"Missing creatorId or imageId parameter."}), 400

    if get_user(data['creatorId']) and get_image(data['imageId']):
        image = get_image(data['imageId'])
        if data['creatorId'] != image.userId:

            prev = get_ranking_by_actors(data['creatorId'], data['imageId'])
            if prev:
                return jsonify({"message":"Current user already ranked this image"}), 409
            ranking = create_ranking(data['creatorId'], data['imageId'], data['score'])
            return jsonify({"message":"Ranking created"}), 200

        return jsonify({"message":"User cannot rank self"}), 409
    return jsonify({"message":"User not found"}), 404

@ranking_views.route('/api/rankings', methods=['GET'])
def get_all_rankings_action():
    args = request.args
    if not args:
        rankings = get_all_rankings_json()
        return jsonify(rankings), 200

    id = args.get('id')
    creatorId = args.get('creatorid')
    imageId = args.get('imageid')
    if id:
        ranking = get_ranking(id)
        if ranking:
            return ranking.toJSON(), 200
        return jsonify({"message":"Ranking Not Found"}), 404
    if creatorId:
        if get_user(creatorId):
            rankings = get_rankings_by_creator(creatorId)
            if rankings:
                return jsonify(rankings), 200
            # Might be removed to return empty list
            return jsonify({"message":"No Rankings by this User"}), 200
        return jsonify({"message":"User Not Found"}), 404
    if imageId:
        if get_image(imageId):
            rankings = get_rankings_by_image(imageId)
            if rankings:
                return jsonify(rankings), 200
            # Might be removed to return empty list
            return jsonify({"message":"No Rankings for this Image"}), 200
        return jsonify({"message":"Image Not Found"}), 404

@ranking_views.route('/api/rankings', methods=['PUT'])
def update_ranking_action():
    data = request.json
    if not data['id'] or not data['score']:
        return jsonify({"message":"Missing id or score parameter."}), 400

    ranking = update_ranking(data['id'], data['score'])
    if ranking:
        return jsonify({"message":"Ranking updated"}), 200
    return jsonify({"message":"Ranking not found"}), 404

@ranking_views.route('/api/rankings/calc', methods=['GET'])
def get_calculated_ranking_action():
    imageId = request.args.get('imageid')
    if not imageId:
        return jsonify({"message":"Missing imageid parameter."}), 400

    if get_image(imageId):
        ranking = get_calculated_ranking(imageId)
        if ranking:
            return jsonify({"calculated_ranking": ranking}), 200
        return jsonify({"message":"No rankings by this image found"}), 200
    return jsonify({"message":"Image not found"}), 404
