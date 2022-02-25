import mariadb as db
import DbInteractions.dbhandler as dbh


def get_comments(tweetId):
    comments = []
    conn, cursor = dbh.db_connect()
    comments_list = []
    try:
        cursor.execute(
            "SELECT comment.id, tweet_id, user_id, username, content, created_at FROM `user` inner join comment on comment.user_id = `user`.id WHERE comment.tweet_id = ?", [tweetId])
        comments = cursor.fetchall()
        for comment in comments:
            comments_list.append({
                'commentId': comment[0],
                'tweetId': comment[1],
                'userId': comment[2],
                'username': comment[3],
                'content': comment[4],
                'createdAt': comment[5]
            })
        dbh.db_disconnect(conn, cursor)
        return True, comments_list
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
