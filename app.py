from flask import Flask, request, Response
import json
import userEndpoint as ue
import traceback

import sys
app = Flask(__name__)

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
        print(Response.data)
        return Response(users_json, mimetype="application/json", status=200)
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
