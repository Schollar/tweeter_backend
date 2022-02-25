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


def post_comment(logintoken, content, tweetId):
    comment = {}
    conn, cursor = dbh.db_connect()
    userId = dbh.get_userId(logintoken)
    try:
        cursor.execute(
            "INSERT INTO comment (user_id, content, tweet_id) VALUES (?, ?, ?)", [userId, content, tweetId])
        conn.commit()
        cursor.execute(
            "SELECT comment.id, comment.tweet_id, comment.user_id, username, content, created_at FROM `user` inner join comment on comment.user_id = `user`.id WHERE content = ?", [content])
        comment = cursor.fetchone()
        comment = {
            'commentId': comment[0],
            'tweetId': comment[1],
            'userId': comment[2],
            'username': comment[3],
            'content': comment[4],
            'createdAt': comment[5]
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, comment


def patch_comment(loginToken, commentId, content):
    comment = {}
    conn, cursor = dbh.db_connect()
    try:
        sql = "UPDATE comment inner join user_session on comment.user_id = user_session.user_id SET content = ? WHERE logintoken = ? and comment.id = ?"
        params = [content, loginToken, commentId]
        cursor.execute(
            sql, params)
        conn.commit()
        cursor.execute(
            "SELECT comment.id, comment.tweet_id, comment.user_id, username, content, created_at FROM `user` inner join comment on comment.user_id = `user`.id WHERE content = ?", [content])
        comment = cursor.fetchone()
        comment = {
            'commentId': comment[0],
            'tweetId': comment[1],
            'userId': comment[2],
            'username': comment[3],
            'content': comment[4],
            'createdAt': comment[5]
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, comment
