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
