from flask import Response, request
import json
import DbInteractions.commentsInteractions as ci

# Function to get comments of a tweet, requests the tweetId and sends it off to the dbinteraction function. If success returns as true, return the response


def get():
    comments_json = None
    success = False
    try:
        tweetId = request.args['tweetId']
        success, comment_list = ci.get_comments(tweetId)
        comments_json = json.dumps(comment_list, default=str)
    except:
        return Response("Something went wrong getting the comments from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(comments_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the comments from the DB!", mimetype="application/json", status=400)

# Function that will create a new comment on a tweet. Requests logintoken, content and tweetId to send to Dbinteractions function. If success comes back as True, return the response.


def post():
    comment_json = None
    success = False
    try:
        logintoken = request.json['loginToken']
        content = request.json['content']
        tweetId = request.json['tweetId']
        success, comment = ci.post_comment(logintoken, content, tweetId)
        comment_json = json.dumps(comment, default=str)
    except:
        return Response("Something went wrong creating a new comment", mimetype="application/json", status=400)
    if(success):
        return Response(comment_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong creating a new comment", mimetype="application/json", status=400)

# Function to change content of a comment. Requests logintoken, commentid and content to send off to dbinteractions function. Convert returned data to json and return the response if success comes back true


def patch():
    comment_json = None
    success = False
    try:
        logintoken = request.json['loginToken']
        commentId = request.json['commentId']
        content = request.json['content']
        success, comment = ci.patch_comment(logintoken, commentId, content)
        comment_json = json.dumps(comment, default=str)
    except:
        return Response("Something went wrong editing the comment.", mimetype="application/json", status=400)
    if(success):
        return Response(comment_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong editing the comment", mimetype="application/json", status=400)

# Function to delete a comment. Requests logintoken and comment Id to send to Dbinteractions function. If success comes back as true return the response with Nothing in it.


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        commentId = request.json['commentId']
        success = ci.delete_comment(logintoken, commentId)
    except:
        return Response("Something went wrong deleting this comment", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong deleting this comment", mimetype="application/json", status=400)
