from flask import request, Response
import json
import DbInteractions.userEndpoint as ue
import DbInteractions.dbhandler as dbh
import secrets
import hashlib


# Function to create password salts


def create_salt():
    return secrets.token_urlsafe(10)

# This endpoint takes in an optional user id. If no Id is sent it will get ALL users from DB back. If ID is sent only info about that user is sent back.


def get():
    users_json = None
    success = False
    try:
        user_id = request.args.get('user_id')
        success, user_list = ue.get_users(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)

# This endpoint will update user information based on what is sent to it. All optional except for logintoken which is required, you can send info seperatly or all at once.


def patch():
    user_json = None
    success = False
    try:
        loginToken = request.json['logintoken']
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        imageUrl = request.json.get('imageUrl')
        bannerUrl = request.json.get('bannerUrl')
        email = request.json.get('email')
        username = request.json.get('username')
        success, user = ue.patch_user(
            loginToken, bio, birthdate, imageUrl, bannerUrl, email, username)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)

# This endpoint will delete a user from the DB. it takes in a password and login token, and if matching will return nothing indicating user no longer exits on planet.


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        password = request.json['password']
        pass_hash = dbh.get_password(password, logintoken=logintoken)
        success = ue.delete_user(logintoken, pass_hash)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)

# This endpoint creates a new user. It takes in a bunch of data that is required and two optional peices of data. It also creates a salt for the user and hashes the salted password. If successfull we get our new user information as a response.


def post():
    user_json = None
    success = False
    try:
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        imageUrl = request.json.get('imageUrl')
        bannerUrl = request.json.get('bannerUrl')
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        salt = create_salt()
        password = salt + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        success, user = ue.post_user(
            bio, birthdate, imageUrl, bannerUrl, email, username, pass_hash, salt)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
