from flask import Response, request
import json
import DbInteractions.commentsInteractions as ci


def get():
    comments_json = None
    success = False
    try:
        tweetId = request.args['tweetId']
        success, comment_list = ci.get_comments(tweetId)
        comments_json = json.dumps(comment_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(comments_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


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
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(comment_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


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
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(comment_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
