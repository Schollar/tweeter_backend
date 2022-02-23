from flask import Flask, request, Response
import json
import userEndpoint as ue
import traceback
import hashlib
import secrets
import userLogin as ul
import userFollows as uf
import dbhandler as dbh

import sys
app = Flask(__name__)

# Function to create password salts


def create_salt():
    return secrets.token_urlsafe(10)

######### USER ENDPOINT ########

# This endpoint takes in an optional user id. If no Id is sent it will get ALL users from DB back. If ID is sent only info about that user is sent back.


@app.get('/api/users')
def get_users():
    user_list = []
    users_json = None
    user_id = None
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

# This endpoint will update user information based on what is sent to it. All optional, you can send info seperatly or all at once.


@app.patch('/api/users')
def patch_user():
    user = None
    loginToken = None
    bio = None
    birthdate = None
    imageUrl = None
    bannerUrl = None
    email = None
    username = None
    success = False
    try:
        loginToken = request.json.get('logintoken')
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


@app.delete('/api/users')
def delete_user():
    logintoken = None
    password = None
    pass_hash = None
    success = False
    try:
        logintoken = request.json.get('loginToken')
        password = request.json.get('password')
        pass_hash = dbh.get_password(password, None, None, logintoken)
        success = ue.delete_user(logintoken, pass_hash)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


@app.post('/api/users')
def post_user():
    user = None
    bio = None
    birthdate = None
    imageUrl = None
    bannerUrl = None
    email = None
    username = None
    password = None
    success = False
    try:
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        imageUrl = request.json.get('imageUrl')
        bannerUrl = request.json.get('bannerUrl')
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        salt = create_salt()
        password = salt + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        success, user = ue.post_user(
            bio, birthdate, imageUrl, bannerUrl, email, username, pass_hash, salt)
        user_json = json.dumps(user, default=str)
    except:
        traceback.print_exc()
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


@app.get('/api/follows')
def get_follows():
    user_list = None
    users_json = None
    user_id = None
    success = False
    try:
        user_id = request.args.get('userId')
        success, user_list = uf.get_follows(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        traceback.print_exc()
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)

######## LOGIN ENDPOINT #######

# Delete endpoint, takes in a login token, upon success it deletes row from user session table(logs user out)


@app.delete('/api/login')
def delete_login():
    logintoken = None
    success = False
    try:
        logintoken = request.json.get('logintoken')
        success = ul.delete_login(logintoken)
    except:
        traceback.print_exc()
        return Response("Something went wrong with logging out", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong with logging out", mimetype="application/json", status=400)


@app.post('/api/login')
def post_login():
    email = None
    username = None
    password = None
    pass_hash = None
    logintoken = None
    success = False
    try:
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        pass_hash = dbh.get_password(password, email, username, logintoken)
        success, user = ul.post_login(
            email, username, pass_hash)
        user_json = json.dumps(user, default=str)
    except:
        traceback.print_exc()
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


# Checking to see if a mode was passed to the script
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print('You must pass a mode to run this script. Either testing or production')
    exit()
# Depending on what mode is passed, we check and run the appropriate code.
if(mode == "testing"):
    print('Running in testing mode!')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode == "production"):
    print('Running in production mode')
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5005)
else:
    print('Please Run in either testing or production')
