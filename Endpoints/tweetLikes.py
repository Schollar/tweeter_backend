from flask import Response, request
import DbInteractions.tweetLikes as tl
import json


def get():
    likes_json = None
    success = False
    try:
        tweetId = request.args.get('tweetId')
        success, like_list = tl.get_tweet_likes(tweetId)
        likes_json = json.dumps(like_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(likes_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


def post():
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        success = tl.post_like(logintoken, tweetId)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        success = tl.delete_like(logintoken, tweetId)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
