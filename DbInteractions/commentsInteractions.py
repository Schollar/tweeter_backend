import mariadb as db
import DbInteractions.dbhandler as dbh

# Function get all comments from a specific tweet. tweetId is taken as an argument


def get_comments(tweetId):
    comments = []
    conn, cursor = dbh.db_connect()
    comments_list = []
    try:
        # Statement that selects information about comments of a tweet, based on the tweet.id matching what is passed to it.
        cursor.execute(
            "SELECT comment.id, tweet_id, user_id, username, content, created_at FROM `user` inner join comment on comment.user_id = `user`.id WHERE comment.tweet_id = ?", [tweetId])
        # Here we get all the row(s) sent to us and then change the data before disconnecting our DB connection and returning the data
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

# Function that creates a new comment on a tweet. takes logintoken, content and tweetId as arguments


def post_comment(logintoken, content, tweetId):
    comment = {}
    conn, cursor = dbh.db_connect()
    userId = dbh.get_userId(logintoken)
    try:
        # Insert into the comment table with the values passed to us and commit.
        cursor.execute(
            "INSERT INTO comment (user_id, content, tweet_id) VALUES (?, ?, ?)", [userId, content, tweetId])
        conn.commit()
        # Run a select statement to get the newly created comment's information, store that information in a variable and then change the data to be an object before disconnecting and returning the data
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

# Function that changes the content of a comment if both logintoken and commentid are valid.(User has to own comment and comment must exist to be valid)


def patch_comment(loginToken, commentId, content):
    comment = {}
    conn, cursor = dbh.db_connect()
    try:
        # Setting up our statement and params, exectuing them and commiting to DB
        sql = "UPDATE comment inner join user_session on comment.user_id = user_session.user_id SET content = ? WHERE logintoken = ? and comment.id = ?"
        params = [content, loginToken, commentId]
        cursor.execute(
            sql, params)
        conn.commit()
        # Run another select statement to grab info on the newly changed comment, then store that info in a variable before changing it into an object.  Then disconnect from DB and return data
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

# Function that will delete a comment if both logintoken and comment Id are valid.(User must own comment, and comment must exist for both to be valid)


def delete_comment(logintoken, commentId):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement to delete comment from DB based on the values passed to us. Commit, disconnect and return True to validate success
        cursor.execute(
            "DELETE comment FROM comment inner join user_session on comment.user_id = user_session.user_id WHERE comment.id = ? and logintoken = ? ", [commentId, logintoken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
