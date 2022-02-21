import mariadb as db
import dbhandler as dbh
import userLogin as ul
import hashlib


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
# I need to check if any values of user object is None, and update based on what has value and skip what does not.


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
        return True, user
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, user


def post_user(bio, birthdate, imageUrl, bannerUrl, email, username, pass_hash, salt):
    user = []
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "INSERT INTO `user` (bio, birthdate, email, username, password, salt) VALUES (?, ?, ?, ?, ?, ?)", [bio, birthdate, email, username, pass_hash, salt])
        conn.commit()
        if(imageUrl != None):
            cursor.execute(
                "UPDATE `user` SET imageUrl = ? WHERE username = ?", [imageUrl, username])
            conn.commit()
        if(bannerUrl != None):
            cursor.execute(
                "UPDATE `user` SET imageUrl = ? WHERE logintoken = ?", [bannerUrl, username])
            conn.commit()
        user = ul.post_login(email, None, pass_hash)
        login_token = user[1]['loginToken']
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
        return True, user
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True, user


def delete_user(loginToken, password):
    salt = None
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "SELECT salt FROM `user` inner join user_session on user_session.user_id = `user`.id WHERE logintoken = ?", [
                loginToken]
        )
        salt = cursor.fetchone()
        password = salt[0] + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        cursor.execute(
            "DELETE `user` FROM `user` inner join user_session on `user`.id = user_session.user_id WHERE password = ? and logintoken = ? ", [pass_hash, loginToken])
        conn.commit()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    dbh.db_disconnect(conn, cursor)
    return True
