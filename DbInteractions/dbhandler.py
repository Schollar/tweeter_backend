import mariadb as db
import DbInteractions.dbcreds as dbcreds
import hashlib

# Connect function that starts a DB connection and creates a cursor


def db_connect():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                          host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print('Something is wrong with the DB')
    except:
        print('Something went wrong connecting to the DB')
    return conn, cursor

# Disconnect function that takes in the conn and cursor and attempts to close both


def db_disconnect(conn, cursor):
    try:
        cursor.close()
    except:
        print('Error closing cursor')
    try:
        conn.close()
    except:
        print('Error closing connection')

# Function that will take in the user input password, and either a username, email or logintoken to get the salt for said user.


def get_password(password, email=None, username=None, logintoken=None):
    salt = None
    pass_hash = None
    conn, cursor = db_connect()
    try:
        # Check to see which of the three arguments does not equal None. They all run a select statement to get the salt for the user, based on either logintoken, email or username
        if(logintoken != None):
            cursor.execute(
                "SELECT salt FROM `user` inner join user_session on user_session.user_id = `user`.id WHERE logintoken = ?", [
                    logintoken])
        elif(email != None):
            cursor.execute("SELECT salt FROM `user`  WHERE email = ?", [email])
        elif(username != None):
            cursor.execute(
                "SELECT salt FROM `user`  WHERE username = ?", [username])
        # After one of the three if statements above has ran, we select the salt, append it to the password and then get the hashed password.
        salt = cursor.fetchone()
        password = salt[0] + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    # Disconnect and return hashed+salted password
    db_disconnect(conn, cursor)
    return pass_hash

# Function that will get a userId from the logintoken passed to it.


def get_userId(logintoken):
    conn, cursor = db_connect()
    try:
        # Select statement to get userId based off logintoken.
        cursor.execute(
            "SELECT `user`.id FROM user inner join user_session on `user`.id = user_session.user_id WHERE logintoken = ?", [logintoken])
        # Save Id to variable, but since it defaults to a list, we then save the variable equal to the list index item 0. Disconnect and return userId
        userId = cursor.fetchone()
        userId = userId[0]
        db_disconnect(conn, cursor)
        return userId
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
