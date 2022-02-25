from flask import Response, request
import DbInteractions.commentLikesInteractions as cl
import json


def get():
    likes_json = None
    success = False
    try:
        commentId = request.args.get('commentId')
        success, like_list = cl.get_comment_likes(commentId)
        likes_json = json.dumps(like_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(likes_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
