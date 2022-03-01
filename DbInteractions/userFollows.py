
import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback

# Function to get the followers of a specific user. Requires a userId as an argument.


def get_follows(userId):
    follows_list = []
    conn, cursor = dbh.db_connect()
    try:
        # Select statement to select the users information that follow the userId sent, save it to a variable before changing the data to an object, disconnecting and returning the data.
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

# Function to create a new follow on a user, login token and follow id must be valid(user must be logged in and user to follow must exist)


def post_follow(logintoken, followId):
    conn, cursor = dbh.db_connect()
    try:
        # Using the get userid helper fucntion to get the userId from the logged in user. Insert statement to insert follow into DB. Commit, disconnect and return true
        userId = dbh.get_userId(logintoken)
        cursor.execute(
            "INSERT INTO follow (user_id, follow_id) VALUES (?, ?)", [userId, followId])
        conn.commit()
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
    return True

# Function to delete a follow. same arguments as function above, runs a Delete statement to delete follow relashionship. Commit, disconnect and return true.


def delete_follow(logintoken, followId):
    userId = None
    conn, cursor = dbh.db_connect()
    try:
        userId = dbh.get_userId(logintoken)
        cursor.execute(
            "DELETE FROM follow WHERE user_id = ? and follow_id = ?", [userId, followId])
        conn.commit()
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
    return True
