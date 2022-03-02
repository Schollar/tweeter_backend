import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback
import secrets

# Function to delete a login token(log a user out)


def delete_login(loginToken):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement, commit disconnect and return true
        cursor.execute(
            "DELETE FROM user_session WHERE logintoken = ? ", [loginToken])
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

# Function that creates a new user session(log a user in)


def post_login(email, username, pass_hash):
    user = []
    userId = None
    conn, cursor = dbh.db_connect()
    try:
        # Check to see wether we are passed the username or email, and based on which does not have a value of None is which statement is ran to get the userId.
        if(email != None):
            cursor.execute(
                "SELECT `user`.id FROM `user` WHERE email = ? and password = ?", [email, pass_hash])
            userId = cursor.fetchone()
            userId = userId[0]
        elif(username != None):
            cursor.execute(
                "SELECT `user`.id FROM `user` WHERE username = ? and password = ?", [username, pass_hash])
            userId = cursor.fetchone()
            userId = userId[0]
        # Insert statement to insert a session to the user_session table based on the userId we get above. Commit the changes
        token = secrets.token_urlsafe(40)
        cursor.execute(
            "INSERT INTO user_session (user_id, logintoken) VALUES (?, ?)", [userId, token])
        conn.commit()
        # Select statement to grab information about the user, aswell as the just created login token, save data to variable change it to an object and return the data
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
    return True, user
