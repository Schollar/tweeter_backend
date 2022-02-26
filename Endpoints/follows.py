from flask import request, Response
import json
import DbInteractions.userFollows as uf


# Function that will get information about users that a specific user follows. Requests the userId of the specific user to send to Dbinteractions file. Convert the returned data to json, if success returns as true, return the converted data in the response

def get():
    users_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, user_list = uf.get_follows(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting the list of users that are followed", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users that are followed", mimetype="application/json", status=400)

# Function that will create a new follow of a user. Requests logintoken and followid(userId of user to follow) to send to dbinteractions function. If success returns true, return a response of none


def post():
    success = False
    try:
        logintoken = request.json['logintoken']
        follow_id = request.json['followId']
        success = uf.post_follow(logintoken, follow_id)
    except:
        return Response("Something went wrong following this user", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong following this user", mimetype="application/json", status=400)

# Function that deletes a follow from a user. Requests logintoken and followId(see above comment) to send to dbinteractions function. If success returns true, return a response of none.


def delete():
    success = False
    try:
        logintoken = request.json['logintoken']
        followId = request.json['followId']
        success = uf.delete_follow(logintoken, followId)
    except:
        return Response("Something went wrong unfollowing this user", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting unfollowing this user", mimetype="application/json", status=400)
