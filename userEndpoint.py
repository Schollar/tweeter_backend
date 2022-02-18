import mariadb as db
import dbhandler as dbh


def get_users(userId):
    users = []
    conn, cursor = dbh.db_connect()
    users_objects = []
    try:
        if(userId != None):
            cursor.execute(
                "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id = ?", [userId])
            users = cursor.fetchone()
            users = {
                'userId': users[0],
                'email': users[1],
                'username': users[2],
                'bio': users[3],
                'birthdate': users[4],
                'imageUrl': users[5],
                'bannerUrl': users[6]
            }
            return True, users
        else:
            cursor.execute(
                "SELECT * FROM user")
            users = cursor.fetchall()
            for user in users:
                users_objects.append(
                    {
                        'userId': user[0],
                        'email': user[1],
                        'username': user[2],
                        'bio': user[3],
                        'birthdate': user[4],
                        'imageUrl': user[5],
                        'bannerUrl': user[6]
                    })
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, users_objects
