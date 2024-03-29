
import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback

# Function that will get users that follow a specific userId


def get_followers(userId):
    follows_list = []
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "SELECT `user`.id, email, username, bio, birthdate, imageUrl, bannerUrl FROM follow inner join `user` on follow.user_id = `user`.id WHERE follow_id = ?", [userId])
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
    except db.OperationalError:
        traceback.print_exc()
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    dbh.db_disconnect(conn, cursor)
    return True, follows_list
