from flask import request, Response
import json
import DbInteractions.userFollowers as uf


def get():
    users_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, user_list = uf.get_followers(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
