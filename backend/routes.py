from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return data"""
    if data:
        return jsonify(data), 200
    
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return picture by id"""
    if data:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        return {"message": "Not Found"}, 404
    
    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """ add picture to data list """
    if data:
        picture = request.json
        for pic in data:
            if picture['id'] == pic['id']:
                return {"Message": f"picture with id {picture['id']} already present"}, 302
        data.append(picture)
        return jsonify(picture), 201

    return {"message": "Internal server error"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if data:
        new_picture = request.json
        new_id = new_picture.get('id')
        for pic in data:
            if pic['id']==new_id and new_picture.get('pic_url'):
                pic.update(new_picture) 
                return new_picture, 200
        return {"message": "picture not found"}, 404

    return {"message": "Internal server error"}, 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204
    return {"message": "picture not found"}, 404
