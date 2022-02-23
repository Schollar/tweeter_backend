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
