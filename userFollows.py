
import mariadb as db
import dbhandler as dbh


def get_follows(userId):
    users = []
    follows_list = []
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "SELECT `user`.id, email, username, bio, birthdate, imageUrl, bannerUrl FROM follow inner join `user` on follow.follow_id = `user`.id WHERE user_id = ?", [userId])
        users = cursor.fetchall()
        for user in users:
            follows_list.append(
                {
                    'userId': user[0],
                    'email': user[1],
                    'username': user[2],
                    'bio': user[3],
                    'birthdate': user[4],
                    'imageUrl': user[5],
                    'bannerUrl': user[6]
                })
        return True, follows_list
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, follows_list
