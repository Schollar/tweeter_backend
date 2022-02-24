import mariadb as db
import DbInteractions.dbhandler as dbh


def get_tweets(userId):
    tweets = []
    conn, cursor = dbh.db_connect()
    tweets_list = []
    try:
        if(userId != None):
            cursor.execute(
                "SELECT tweet.id, userId, username, content, created_at, tweet.imageUrl, `user`.imageUrl FROM `user` inner join tweet on tweet.userId = `user`.id WHERE `user`.id = ?", [userId])
            tweets = cursor.fetchall()
            for tweet in tweets:
                tweets_list = {
                    'tweetId': tweet[0],
                    'userId': tweet[1],
                    'username': tweet[2],
                    'content': tweet[3],
                    'createdAt': tweet[4],
                    'tweetImageUrl': tweet[5],
                    'userImageUrl': tweet[6]

                }
            dbh.db_disconnect(conn, cursor)
            return True, tweets_list
        else:
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


def post_tweet(logintoken, content, imageUrl):
    tweet = {}
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "SELECT `user`.id FROM user inner join user_session on `user`.id = user_session.user_id WHERE logintoken = ?", [logintoken])
        userId = cursor.fetchone()
        userId = userId[0]
        cursor.execute(
            "INSERT INTO tweet (userId, content, imageUrl) VALUES (?, ?, ?)", [userId, content, imageUrl])
        conn.commit()
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


def patch_tweet(loginToken, tweetId, content, imageUrl):
    tweet = {}
    conn, cursor = dbh.db_connect()
    try:
        sql = "UPDATE tweet inner join user_session on tweet.userId = user_session.user_id SET WHERE logintoken = ? and tweet.id = ?"
        params = [loginToken, tweetId]
        if(imageUrl != None):
            sql = sql.replace("SET", "SET imageUrl = ?,")
            params.insert(0, imageUrl)
        if(content != None):
            sql = sql.replace("SET", "SET content = ?,")
            params.insert(0, content)
        sql = sql.replace("?, WHERE", "? WHERE")
        cursor.execute(
            sql, params)
        conn.commit()
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
