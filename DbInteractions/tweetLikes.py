import mariadb as db
import DbInteractions.dbhandler as dbh

# Function that will get either all tweets likes or a specific tweet's likes.


def get_tweet_likes(tweetId):
    tweet_likes = []
    conn, cursor = dbh.db_connect()
    like_list = []
    try:
        # Setting up sql statement and params.
        sql = "SELECT tweet_like.tweet_id, `user`.id, `user`.username FROM `user` inner join tweet_like on `user`.id = tweet_like.user_id"
        params = []
        # If tweetId is not None, change the sql statement and params to get likes on a specific tweet
        if(tweetId != None):
            sql = sql.replace("tweet_like.user_id",
                              "tweet_like.user_id WHERE tweet_like.tweet_id = ?")
            params.insert(0, tweetId)
        # Executing sql statement, saving the rows selected to a variable. Changing the data to be an object before disconnecting and returning the data
        cursor.execute(sql, params)
        tweet_likes = cursor.fetchall()
        for like in tweet_likes:
            like_list.append({
                'tweetId': like[0],
                'userId': like[1],
                'username': like[2],
            })
        dbh.db_disconnect(conn, cursor)
        return True, like_list
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')

# Function that will create a new like for a tweet. Takes in a logintoken and tweetId


def post_like(logintoken, tweetId):
    conn, cursor = dbh.db_connect()
    # using helper function to get the userId
    userId = dbh.get_userId(logintoken)
    try:
        # Inserting a new tweet like into the DB. Commit, disconnect and return true to validate success
        cursor.execute(
            "INSERT INTO tweet_like (tweet_id, user_id) VALUES (?, ?)", [tweetId, userId])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True

# Function that will delete a like from a tweet. Takes a logintoken and tweetId as arguments


def delete_like(logintoken, tweetId):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement to delete a like from a tweet. Both tweetid and logintoken must be valid(user must own like and tweet must exist). Commit, disconnect and return true to validate success
        cursor.execute(
            "DELETE tweet_like FROM tweet_like inner join user_session on tweet_like.user_id = user_session.user_id WHERE tweet_id = ? and logintoken = ?", [tweetId, logintoken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
