import mariadb as db
import DbInteractions.dbhandler as dbh

# Function that gets either all tweets or a specific user's tweets based on userId value


def get_tweets(userId):
    tweets = []
    conn, cursor = dbh.db_connect()
    tweets_list = []
    try:
        # If userId has value we select all tweets from the specific user, save the data to a variable and then change the variable to an object before disconnecting and returning the data
        if(userId != None):
            cursor.execute(
                "SELECT tweet.id, userId, username, content, created_at, tweet.imageUrl, `user`.imageUrl FROM `user` inner join tweet on tweet.userId = `user`.id WHERE `user`.id = ?", [userId])
            tweets = cursor.fetchall()
            for tweet in tweets:
                tweets_list.append({
                    'tweetId': tweet[0],
                    'userId': tweet[1],
                    'username': tweet[2],
                    'content': tweet[3],
                    'createdAt': tweet[4],
                    'tweetImageUrl': tweet[5],
                    'userImageUrl': tweet[6]

                })
            dbh.db_disconnect(conn, cursor)
            return True, tweets_list
        else:
            # If userId value is None, we select all tweets, save them into a list and then change the list to be a list of objects. Disconnect and return the data.
            cursor.execute(
                "SELECT tweet.id, userId, username, content, created_at, tweet.imageUrl, `user`.imageUrl FROM `user` inner join tweet on tweet.userId = `user`.id")
            tweets = cursor.fetchall()
            for tweet in tweets:
                tweets_list.append({
                    'tweetId': tweet[0],
                    'userId': tweet[1],
                    'username': tweet[2],
                    'content': tweet[3],
                    'createdAt': tweet[4],
                    'tweetImageUrl': tweet[5],
                    'userImageUrl': tweet[6]

                })
            dbh.db_disconnect(conn, cursor)
            return True, tweets_list
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')

# Function to create a new tweet, takes in a login token, content and optional imageUrl


def post_tweet(logintoken, content, imageUrl):
    tweet = {}
    conn, cursor = dbh.db_connect()
    userId = dbh.get_userId(logintoken)
    try:
        # Insert statement to insert the values of arguments into the table to create a new tweet then committing.
        cursor.execute(
            "INSERT INTO tweet (userId, content, imageUrl) VALUES (?, ?, ?)", [userId, content, imageUrl])
        conn.commit()
        # Select statement to select the newly created tweet and save it to a variable, change the variable to be an object before disconnecting and returning the data
        cursor.execute(
            "SELECT tweet.id, `user`.id, username, `user`.imageUrl, content, created_at, tweet.imageUrl FROM `user` inner join tweet on tweet.userId = `user`.id WHERE content = ?", [content])
        tweet = cursor.fetchone()
        tweet = {
            'tweetId': tweet[0],
            'userId': tweet[1],
            'username': tweet[2],
            'userImageUrl': tweet[3],
            'content': tweet[4],
            'createdAt': tweet[5],
            'imageUrl': tweet[6]
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, tweet

# Function to update a tweets content or imageUrl  if both logintoken and tweetId are valid(user must own tweet and tweet id must exist for both to be valid)


def patch_tweet(loginToken, tweetId, content, imageUrl):
    tweet = {}
    conn, cursor = dbh.db_connect()
    try:
        # Setting up our sql statement and params
        sql = "UPDATE tweet inner join user_session on tweet.userId = user_session.user_id SET WHERE logintoken = ? and tweet.id = ?"
        params = [loginToken, tweetId]
        # Checking to see if either content or imageUrl are None, if they are not we change up our sql statement and params accordingly
        if(imageUrl != None):
            sql = sql.replace("SET", "SET imageUrl = ?,")
            params.insert(0, imageUrl)
        if(content != None):
            sql = sql.replace("SET", "SET content = ?,")
            params.insert(0, content)
        # This is here in the case that both content and imageUrl are being changed, we have an extra comma so this will remove it.
        sql = sql.replace("?, WHERE", "? WHERE")
        # Executing and committing sql statement
        cursor.execute(
            sql, params)
        conn.commit()
        # Select statement to grab the newly changed tweets information, saving it to a variable and then changing it into an object before disconnecting and returning the data
        cursor.execute(
            "SELECT tweet.id, content, imageUrl FROM tweet WHERE tweet.id = ?", [tweetId])
        tweet = cursor.fetchone()
        tweet = {
            'tweetId': tweet[0],
            'content': tweet[1],
            'imageUrl': tweet[2],
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, tweet

# Function that will delete a tweet if tweetid is valid and user owns tweet.


def delete_tweet(logintoken, tweetId):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement to delete tweet from the DB. Committing, disconnecting and then return true to validate success
        cursor.execute(
            "DELETE tweet FROM tweet inner join user_session on tweet.userId = user_session.user_id WHERE tweet.id = ? and logintoken = ? ", [tweetId, logintoken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
