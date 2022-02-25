import mariadb as db
import DbInteractions.dbhandler as dbh
import DbInteractions.userLogin as ul

# Function that returns all users or a specific user based on the userId value


def get_users(userId):
    users = []
    conn, cursor = dbh.db_connect()
    users_objects = []
    try:
        # Checking to see if userId is none, if not we return the information about that specific user
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
            dbh.db_disconnect(conn, cursor)
            return True, users
        else:
            # If userid is none, we get all information on all users, in both cases we save the data to a variable, change it to an object above, or list of objects below before disconnecting and returning the data
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
            dbh.db_disconnect(conn, cursor)
            return True, users_objects
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')

# Function that will change information based on if the values of the arguments are None or not, we check one by one and update one by one, which is less than ideal.


def patch_user(loginToken, bio, birthdate, imageUrl, bannerUrl, email, username):
    user = []
    conn, cursor = dbh.db_connect()
    try:
        if(bio != None):
            cursor.execute(
                "UPDATE `user` inner join user_session on `user`.id = user_session.user_id SET bio = ? WHERE logintoken = ?", [bio, loginToken])
            conn.commit()
        if(birthdate != None):
            cursor.execute(
                "UPDATE `user` inner join user_session on `user`.id = user_session.user_id SET birthdate = ? WHERE logintoken = ?", [birthdate, loginToken])
            conn.commit()
        if(imageUrl != None):
            cursor.execute(
                "UPDATE `user` inner join user_session on `user`.id = user_session.user_id SET imageUrl = ? WHERE logintoken = ?", [imageUrl, loginToken])
            conn.commit()
        if(bannerUrl != None):
            cursor.execute(
                "UPDATE `user` inner join user_session on `user`.id = user_session.user_id SET bannerUrl = ? WHERE logintoken = ?", [bannerUrl, loginToken])
            conn.commit()
        if(email != None):
            cursor.execute(
                "UPDATE `user` inner join user_session on `user`.id = user_session.user_id SET email = ? WHERE logintoken = ?", [email, loginToken])
            conn.commit()
        if(username != None):
            cursor.execute(
                "UPDATE `user` inner join user_session on `user`.id = user_session.user_id SET username = ? WHERE logintoken = ?", [username, loginToken])
            conn.commit()
        # After all updates and commits are done, a select statement runs to get the information on the newly updated user. Save the data to a variable and change it to an object before disconnecting and returning the data
        cursor.execute(
            "SELECT `user`.id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user inner join user_session on `user`.id = user_session.user_id WHERE logintoken = ?", [loginToken])
        user = cursor.fetchone()
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2],
            'bio': user[3],
            'birthdate': user[4],
            'imageUrl': user[5],
            'bannerUrl': user[6]
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, user

# Function that will create a new user. Takes multiple arguments.


def post_user(bio, birthdate, imageUrl, bannerUrl, email, username, pass_hash, salt):
    user = []
    conn, cursor = dbh.db_connect()
    try:
        # Inserting a new user into the DB with the values from the arguments and then commit
        cursor.execute(
            "INSERT INTO `user` (bio, birthdate, email, username, password, salt) VALUES (?, ?, ?, ?, ?, ?)", [bio, birthdate, email, username, pass_hash, salt])
        conn.commit()
        # Since imageUrl and bannerUrl are optional, after creating the new user, we check to see if the values are none, if not we update the new user to the values from the arguments.
        if(imageUrl != None):
            cursor.execute(
                "UPDATE `user` SET imageUrl = ? WHERE username = ?", [imageUrl, username])
            conn.commit()
        if(bannerUrl != None):
            cursor.execute(
                "UPDATE `user` SET imageUrl = ? WHERE logintoken = ?", [bannerUrl, username])
            conn.commit()
        # After creating the user in the DB, we pass in information to the user login endpoint to also log the user in after creation, creating a login token.
        user = ul.post_login(email, None, pass_hash)
        # Saving the login token to a variable
        login_token = user[1]['loginToken']
        # Run a select statement to get data on the newly created user, save it to a variable and then change to an object, with the logintoken aswell. before disconnecting and returning the data
        cursor.execute(
            "SELECT `user`.id, email, username, bio, birthdate, imageUrl, bannerUrl FROM `user` WHERE username = ?", [username])
        user = cursor.fetchone()
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2],
            'bio': user[3],
            'birthdate': user[4],
            'imageUrl': user[5],
            'bannerUrl': user[6],
            'loginToken': login_token
        }
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, user

# Function that will delete a user. Takes in login token and hashed password as arguments


def delete_user(loginToken, pass_hash):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement that deletes a user from the DB if login token and password are valid(password is correct and user is logged in). Commit, disconnect and return true to validate success
        cursor.execute(
            "DELETE `user` FROM `user` inner join user_session on `user`.id = user_session.user_id WHERE password = ? and logintoken = ? ", [pass_hash, loginToken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
