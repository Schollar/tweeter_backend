from flask import Flask
import Endpoints.users as users
import Endpoints.login as login
import Endpoints.follows as follows
import Endpoints.followers as followers
import Endpoints.tweets as tweets
import Endpoints.tweetLikes as tlikes
import Endpoints.comments as comments
import Endpoints.commentlikes as commentlikes

import sys
app = Flask(__name__)

# ENDPOINT README###$
# These endpoint all create a function, which returns the
# information from the actual function that is imported and called from another file.
# All endpoints are split up into their own respective files for organizational sake.

## USER ENDPOINT ##


@app.get('/api/users')
def get_users():
    return users.get()


@app.patch('/api/users')
def patch_users():
    return users.patch()


@app.delete('/api/users')
def delete_user():
    return users.delete()


@app.post('/api/users')
def post_user():
    return users.post()

######### FOLLOW ENDPOINT ########


@app.get('/api/follows')
def get_follows():
    return follows.get()


@app.post('/api/follows')
def post_follow():
    return follows.post()


@app.delete('/api/follows')
def delete_follow():
    return follows.delete()


@app.get('/api/followers')
def get_followers():
    return followers.get()
######## LOGIN ENDPOINT #######


@app.delete('/api/login')
def delete_login():
    return login.delete()


@app.post('/api/login')
def post_login():
    return login.post()

#####TWEETS Endpoint####


@app.get('/api/tweets')
def get_tweets():
    return tweets.get()


@app.post('/api/tweets')
def post_tweet():
    return tweets.post()


@app.patch('/api/tweets')
def patch_tweet():
    return tweets.patch()


@app.delete('/api/tweets')
def delete_tweet():
    return tweets.delete()

#### TWEET LIKES ENDPOINT ####


@app.get('/api/tweet-likes')
def get_tweet_likes():
    return tlikes.get()


@app.post('/api/tweet-likes')
def post_tweet_like():
    return tlikes.post()


@app.delete('/api/tweet-likes')
def delete_tweet_like():
    return tlikes.delete()


#### COMMENTS ENDPOINT ####
@app.get('/api/comments')
def get_comments():
    return comments.get()


@app.post('/api/comments')
def post_comment():
    return comments.post()


@app.patch('/api/comments')
def patch_comment():
    return comments.patch()


@app.delete('/api/comments')
def delete_comment():
    return comments.delete()

#### COMMENT LIKES ENDPOINTS ####


@app.get('/api/comment-likes')
def get_comment_likes():
    return commentlikes.get()


@app.post('/api/comment-likes')
def post_comment_like():
    return commentlikes.post()


@app.delete('/api/comment-likes')
def delete_comment_like():
    return commentlikes.delete()


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
    bjoern.run(app, "0.0.0.0", 5006)
else:
    print('Please Run in either testing or production')
