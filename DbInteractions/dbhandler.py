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


def get_password(password, email=None, username=None, logintoken=None):
    salt = None
    pass_hash = None
    conn, cursor = db_connect()
    try:
        if(logintoken != None):
            cursor.execute(
                "SELECT salt FROM `user` inner join user_session on user_session.user_id = `user`.id WHERE logintoken = ?", [
                    logintoken])
        elif(email != None):
            cursor.execute("SELECT salt FROM `user`  WHERE email = ?", [email])
        elif(username != None):
            cursor.execute(
                "SELECT salt FROM `user`  WHERE username = ?", [username])
        salt = cursor.fetchone()
        password = salt[0] + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
    except db.OperationalError:
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    db_disconnect(conn, cursor)
    return pass_hash
