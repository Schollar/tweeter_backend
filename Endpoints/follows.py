from flask import request, Response
import json
import DbInteractions.userFollows as uf


# This endpoint takes in a user Id and gets user's information returned that follow said user.


def get():
    users_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, user_list = uf.get_follows(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


def post():
    success = False
    try:
        logintoken = request.json['logintoken']
        follow_id = request.json['followId']
        success = uf.post_follow(logintoken, follow_id)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
