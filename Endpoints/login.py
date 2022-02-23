from flask import request, Response
import DbInteractions.userLogin as ul
import DbInteractions.dbhandler as dbh
import json

# Delete endpoint, takes in a login token, upon success it deletes row from user session table(logs user out)


def delete():
    success = False
    try:
        logintoken = request.json['logintoken']
        success = ul.delete_login(logintoken)
    except:
        return Response("Something went wrong with logging out", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong with logging out", mimetype="application/json", status=400)

# POST login endpoint takes in either username or email and a password, and creates a new user session, user information along with a new login token is return upon success


def post():
    user_json = None
    success = False
    try:
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json['password']
        pass_hash = dbh.get_password(password, email=email, username=username)
        success, user = ul.post_login(
            email, username, pass_hash)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of users from the DB!", mimetype="application/json", status=400)
