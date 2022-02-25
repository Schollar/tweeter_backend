from flask import Response, request
import DbInteractions.tweetEndpoint as te
import json


def get():
    tweets_json = None
    success = False
    try:
        user_id = request.args.get('user_id')
        success, tweet_list = te.get_tweets(user_id)
        tweets_json = json.dumps(tweet_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(tweets_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


def post():
    tweet_json = None
    success = False
    try:
        logintoken = request.json['logintoken']
        content = request.json['content']
        imageUrl = request.json.get('imageUrl')
        success, tweet = te.post_tweet(logintoken, content, imageUrl)
        tweet_json = json.dumps(tweet, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(tweet_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


def patch():
    tweet_json = None
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        content = request.json.get('content')
        imageUrl = request.json.get('imageUrl')
        success, tweet = te.patch_tweet(logintoken, tweetId, content, imageUrl)
        tweet_json = json.dumps(tweet, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(tweet_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        success = te.delete_tweet(logintoken, tweetId)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
