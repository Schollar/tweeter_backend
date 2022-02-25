import mariadb as db
import DbInteractions.dbhandler as dbh

# Function to get comment likes. Takes in commentId.


def get_comment_likes(commentId):
    comment_likes = []
    conn, cursor = dbh.db_connect()
    like_list = []
    try:
        # Here we setup our statment and params
        sql = "SELECT comment_like.comment_id, `user`.id, `user`.username FROM `user` inner join comment_like on `user`.id = comment_like.user_id"
        params = []
        # Check to see if commentId has value, if it does we change up our sql statement accordingly and add commentId to params.
        if(commentId != None):
            sql = sql.replace("comment_like.user_id",
                              "comment_like.user_id WHERE comment_like.comment_id = ?")
            params.insert(0, commentId)
        # If commentId is None we skip to this step. This is where we actually execute our sql statement with the params.
        cursor.execute(sql, params)
        # Use fetchall because sometimes we have more than one row being returned to us.
        comment_likes = cursor.fetchall()
        # Loop through to make the data what we want it to be, a list of objects.
        for like in comment_likes:
            like_list.append({
                'commentId': like[0],
                'userId': like[1],
                'username': like[2],
            })
        # Disconnect and return the information we just grabbed from the DB
        dbh.db_disconnect(conn, cursor)
        return True, like_list
    except db.OperationalError:
        print('Something went wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')

# Function that creates a new like for a comment. Takes in a login token and commentId as arguments


def post_comment_like(logintoken, commentId):
    like = {}
    conn, cursor = dbh.db_connect()
    # Get our userId by using our helper function passing in the logintoken
    userId = dbh.get_userId(logintoken)
    try:
        # Execute and commit the sql statement that inserts values into the comment like table
        cursor.execute(
            "INSERT INTO comment_like (user_id, comment_id) VALUES (?, ?)", [userId, commentId])
        conn.commit()
        # Select the newly created comment to return
        cursor.execute("SELECT comment_id, user_id, username FROM comment_like inner join `user` on `user`.id = user_id WHERE comment_id = ? and user_id = ?", [
                       commentId, userId])
        # Grab the row selected from the sql statement, change the data into object
        like = cursor.fetchone()
        like = {
            'commentId': like[0],
            'userId': like[1],
            'username': like[2],
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    # Disconnect and return the information
    dbh.db_disconnect(conn, cursor)
    return True, like

# Function deletes a like from a comment. Takes in a login token and commentId as arguments


def delete_like(logintoken, commentId):
    conn, cursor = dbh.db_connect()
    try:
        # Statement deletes a like from the comment like table if both the commentId and logintoken are valid. Use a innerjoin with user_session to match up logintoken
        cursor.execute(
            "DELETE comment_like FROM comment_like inner join user_session on comment_like.user_id = user_session.user_id WHERE comment_id = ? and logintoken = ?", [commentId, logintoken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    # Return true to signify success
    return True
