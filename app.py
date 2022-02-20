from flask import Flask, request, Response
import json
import userEndpoint as ue
import traceback
import hashlib
import secrets

import sys
app = Flask(__name__)


def create_salt():
    return secrets.token_urlsafe(10)
# Function that takes in no user input, runs the dbhandler get users which gets all the users from the db and returns them in the response


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
        traceback.print_exc()
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


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
        traceback.print_exc()
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)


@ app.delete('/api/users')
def delete_user():
    logintoken = None
    salt = None
    password = None
    success = False
    try:
        logintoken = request.json('loginToken')
        password = request.json('password')
        salt = create_salt()
        password = salt + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        success = ue.get_users(logintoken, pass_hash)
    except:
        traceback.print_exc()
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response
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
