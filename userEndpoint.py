import mariadb as db
import dbhandler as dbh


def get_users(userId):
    users = []
    conn, cursor = dbh.db_connect()
    try:
        if(userId != None):
            cursor.execute(
                "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id = ?", [userId])
            users = cursor.fetchone()
        else:
            cursor.execute(
                "SELECT * FROM user")
            users = cursor.fetchall()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, users
