from flask import Response, request
import DbInteractions.commentLikesInteractions as cl
import json

# Function to get comment likes. Takes in commentId as argument, can be None if we want all likes.
# Sends user input to DBinteraction function, and if success returns true from DBinteraction, return the response data


def get():
    likes_json = None
    success = False
    try:
        commentId = request.args('commentId')
        success, like_list = cl.get_comment_likes(commentId)
        likes_json = json.dumps(like_list, default=str)
    except:
        return Response("Something went wrong getting the comment likes.", mimetype="application/json", status=400)
    if(success):
        return Response(likes_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the comment likes.", mimetype="application/json", status=400)

# Function to create a new like on a comment. Takes in a logintoken and commentId to send off to Dbinteraction function. If success comes back true, return the response


def post():
    like_json = []
    success = False
    try:
        logintoken = request.json['loginToken']
        commentId = request.json['commentId']
        success, like = cl.post_comment_like(logintoken, commentId)
        like_json = json.dumps(like, default=str)
    except:
        return Response("Something went wrong liking this comment", mimetype="application/json", status=400)
    if(success):
        return Response(like_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong liking this comment", mimetype="application/json", status=400)

# Function to delete like from a comment, the same as function above but does the opposite.
# Return Nothing on a successful delete


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        commentId = request.json['commentId']
        success = cl.delete_like(logintoken, commentId)
    except:
        return Response("Something went wrong deleting this comment", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong deleting this comment", mimetype="application/json", status=400)
