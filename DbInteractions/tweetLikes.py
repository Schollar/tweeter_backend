import mariadb as db
import DbInteractions.dbhandler as dbh


def get_tweet_likes(tweetId):
    tweet_likes = []
    conn, cursor = dbh.db_connect()
    like_list = []
    try:
        sql = "SELECT tweet_like.tweet_id, `user`.id, `user`.username FROM `user` inner join tweet_like on `user`.id = tweet_like.user_id"
        params = []
        if(tweetId != None):
            sql = sql.replace("tweet_like.user_id",
                              "tweet_like.user_id WHERE tweet_like.tweet_id = ?")
            params.insert(0, tweetId)
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


def post_like(logintoken, tweetId):
    conn, cursor = dbh.db_connect()
    userId = dbh.get_userId(logintoken)
    try:
        cursor.execute(
            "INSERT INTO tweet_like (tweet_id, user_id) VALUES (?, ?)", [tweetId, userId])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
