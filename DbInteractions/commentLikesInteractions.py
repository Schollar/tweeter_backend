import mariadb as db
import DbInteractions.dbhandler as dbh


def get_comment_likes(commentId):
    comment_likes = []
    conn, cursor = dbh.db_connect()
    like_list = []
    try:
        sql = "SELECT comment_like.comment_id, `user`.id, `user`.username FROM `user` inner join comment_like on `user`.id = comment_like.user_id"
        params = []
        if(commentId != None):
            sql = sql.replace("comment_like.user_id",
                              "comment_like.user_id WHERE comment_like.comment_id = ?")
            params.insert(0, commentId)
        cursor.execute(sql, params)
        comment_likes = cursor.fetchall()
        for like in comment_likes:
            like_list.append({
                'commentId': like[0],
                'userId': like[1],
                'username': like[2],
            })
        dbh.db_disconnect(conn, cursor)
        return True, like_list
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')


def post_comment_like(logintoken, commentId):
    like = {}
    conn, cursor = dbh.db_connect()
    userId = dbh.get_userId(logintoken)
    try:
        cursor.execute(
            "INSERT INTO comment_like (user_id, comment_id) VALUES (?, ?)", [userId, commentId])
        conn.commit()
        cursor.execute("SELECT comment_id, user_id, username FROM comment_like inner join `user` on `user`.id = user_id WHERE comment_id = ? and user_id = ?", [
                       commentId, userId])
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
    dbh.db_disconnect(conn, cursor)
    return True, like


def delete_like(logintoken, commentId):
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "DELETE comment_like FROM comment_like inner join user_session on comment_like.user_id = user_session.user_id WHERE comment_id = ? and logintoken = ?", [commentId, logintoken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
