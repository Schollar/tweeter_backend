import mariadb as db
import DbInteractions.dbhandler as dbh


def delete_login(loginToken):
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "DELETE FROM user_session WHERE logintoken = ? ", [loginToken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True


def post_login(email, username, pass_hash):
    user = []
    userId = None
    conn, cursor = dbh.db_connect()
    try:
        if(email != None):
            cursor.execute(
                "SELECT `user`.id FROM `user` WHERE email = ? and password = ?", [email, pass_hash])
            userId = cursor.fetchone()
            userId = userId[0]
            cursor.execute(
                "INSERT INTO user_session (user_id) VALUES (?)", [userId])
            conn.commit()
        if(username != None):
            cursor.execute(
                "SELECT `user`.id FROM `user` WHERE username = ? and password = ?", [username, pass_hash])
            userId = cursor.fetchone()
            userId = userId[0]
            cursor.execute(
                "INSERT INTO user_session (user_id) VALUES (?)", [userId])
            conn.commit()
        cursor.execute(
            "SELECT `user`.id, email, username, bio, birthdate, imageUrl, bannerUrl, loginToken FROM `user` inner join user_session on `user`.id = user_session.user_id WHERE `user`.id = ?", [userId])
        user = cursor.fetchone()
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2],
            'bio': user[3],
            'birthdate': user[4],
            'imageUrl': user[5],
            'bannerUrl': user[6],
            'loginToken': user[7]
        }
        return True, user
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, user
