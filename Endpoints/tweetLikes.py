from flask import Response, request
import DbInteractions.tweetLikes as tl
import json

# Function to get either all tweets likes, or a specific tweets likes. Optional request for tweetId if specific tweets likes to send to dbinteractions function. Convert returned data to json, and if success also returned as True, return converted data in response


def get():
    likes_json = None
    success = False
    try:
        tweetId = request.args.get('tweetId')
        success, like_list = tl.get_tweet_likes(tweetId)
        likes_json = json.dumps(like_list, default=str)
    except:
        return Response("Something went wrong getting tweet likes.", mimetype="application/json", status=400)
    if(success):
        return Response(likes_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting tweet likes", mimetype="application/json", status=400)

# Function to create a new like on a tweet. Requests logintoken and tweetid to send to dbinteractions function. If success returns true, return a response with None.


def post():
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        success = tl.post_like(logintoken, tweetId)
    except:
        return Response("Something went wrong liking the tweet", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong liking the tweet", mimetype="application/json", status=400)

# Function to delete a like from a tweet. Requests login token and tweetid to send to dbinteractions function. If success returns as true, return a response of None.


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        success = tl.delete_like(logintoken, tweetId)
    except:
        return Response("Something went wrong removing the like", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong removing the like", mimetype="application/json", status=400)
