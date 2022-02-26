from flask import request, Response
import json
import DbInteractions.userFollowers as uf

# Function to get users that follow another user. requests userId to send to Dbinteractions function. convert data returned to json, and if success is returned as true return the converted data in the response


def get():
    users_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, user_list = uf.get_followers(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting the list of followers", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of followers", mimetype="application/json", status=400)
