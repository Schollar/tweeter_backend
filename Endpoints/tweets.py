from flask import Response, request
import DbInteractions.tweetEndpoint as te
import json

# Function to get either all tweets or a specific user's tweets if a userid is sent. Send data to dbinteractions file. Converted the returned data to json, and if success returns as true, return the data in the response


def get():
    tweets_json = None
    success = False
    try:
        user_id = request.args.get('userId')
        success, tweet_list = te.get_tweets(user_id)
        tweets_json = json.dumps(tweet_list, default=str)
    except:
        return Response("Something went wrong getting the list of tweets", mimetype="application/json", status=400)
    if(success):
        return Response(tweets_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of tweets", mimetype="application/json", status=400)

# Function to create a new tweet. Requires a login token and content, image url is optional. Send the data off to dbinteractions function. Convert the returned data, upon success return the converted data in the response


def post():
    tweet_json = None
    success = False
    try:
        logintoken = request.json['loginToken']
        content = request.json['content']
        imageUrl = request.json.get('imageUrl')
        success, tweet = te.post_tweet(logintoken, content, imageUrl)
        tweet_json = json.dumps(tweet, default=str)
    except:
        return Response("Something went wrong creating a new tweet", mimetype="application/json", status=400)
    if(success):
        return Response(tweet_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong creating a new tweet", mimetype="application/json", status=400)

# Function to edit an existing tweet if user owns it. requires login token and tweet id, with content and imageUrl being optional. Send data to dbinteractions function. Convert returned data
# if successful, return converted data in the response


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
        return Response("Something went wrong editing this tweet", mimetype="application/json", status=400)
    if(success):
        return Response(tweet_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong editing this tweet", mimetype="application/json", status=400)

# Function to delete a tweet if user owns it. Requires login token and tweetId to send to dbinteractions function. if successful, return a response with None.


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        tweetId = request.json['tweetId']
        success = te.delete_tweet(logintoken, tweetId)
    except:
        return Response("Something went wrong deleting this tweet", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong deleting this tweet", mimetype="application/json", status=400)
