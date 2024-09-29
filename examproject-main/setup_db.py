import sqlite3
from sqlite3 import Error
import os
from werkzeug.security import generate_password_hash

# Finner pathen til denne filen
script_dir = os.path.dirname(os.path.abspath(__file__))

# Spesifiserer hvor db-fila er 
database = os.path.join(script_dir, 'data','database.db')


# Oppsettet fra assignment-6 og ex1 forelesning 04.04
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


##### DELETE TABLES ######## 

def delete_table(conn, table_name):
    """
    Delete a table from the database
    :param conn: Connection object
    :param table_name: Name of the table to delete
    """
    try:
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {table_name}")
    except Error as e:
        print(e)


##### CREATE TABLES ######## 

sql_create_admins_table = """CREATE TABLE IF NOT EXISTS admins (
                                admin_id INTEGER PRIMARY KEY,
                                email VARCHAR(50),
                                password_hash VARCHAR(50),
                                first_name VARCHAR(20)
                            );"""

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                email VARCHAR(50),
                                password_hash VARCHAR(50),
                                first_name VARCHAR(20),
                                image TEXT,
                                subscribe BOOLEAN
                            );"""

sql_create_subscriptions_table = """CREATE TABLE IF NOT EXISTS subscriptions (
                                    email VARCHAR(50) PRIMARY KEY,
                                    subscribed BOOLEAN NOT NULL
                                );"""

sql_create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                image IMAGE BLOB NOT NULL,
                                body TEXT NOT NULL,
                                tags TEXT NOT NULL,
                                publish_date TEXT NOT NULL,
                                admin_id INTEGER,
                                FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
                            );"""


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


#### INSERT #########
        
def add_admin(conn, admin_id, email, password_hash, first_name):
    """
    Add a new admin into the admins table
    :param conn:
    :param admin_id:
    :param email:
    :param password_hash:
    :param first_name
    """
    sql = ''' INSERT INTO admins(admin_id, email, password_hash, first_name)
              VALUES(?,?,?,?) '''
    try:
        password_hash = generate_password_hash(password_hash)
        cur = conn.cursor()
        cur.execute(sql, (admin_id, email, password_hash, first_name))
        conn.commit()
    except Error as e:
        print(e)


def init_admins(conn):
    init = [(1, "sofie@gmail.com", "sofie1234", "Sofie"),
            (2, "paulina@gmail.com", "paulina1234", "Paulina"),
            (3, "anette@gmail.com", "anette1234", "Anette"),
            (4, "lisbeth@gmail.com", "lisbeth1234", "Lisbeth")]
    for s in init:
        add_admin(conn, s[0], s[1], s[2], s[3])


def add_user(conn, user_id, email, password_hash, first_name, image, subscribe):
    """
    Add a new user into the users table
    :param conn:
    :param user_id:
    :param email:
    :param password_hash:
    :param first_name:
    :param image:
    :param subscribe:
    """
    sql = ''' INSERT INTO users(user_id, email, password_hash, first_name, image, subscribe)
              VALUES(?,?,?,?,?,?) '''
    try:
        password_hash = generate_password_hash(password_hash)
        cur = conn.cursor()
        cur.execute(sql, (user_id, email, password_hash, first_name, image, subscribe))
        conn.commit()
    except Error as e:
        print(e)
        

def init_users(conn):
    init = [(1, "sofie@gmail.com", "sofie1234", "Sofie", "static/images/sofie.jpeg", True),
            (2, "paulina@gmail.com", "paulina1234", "Paulina", "static/images/paulina.jpeg", True),
            (3, "anette@gmail.com", "anette1234", "Anette", "static/images/anette.jpeg", True),
            (4, "lisbeth@gmail.com", "lisbeth1234", "Lisbeth", "static/images/sofie.avif", True),
            (5, "dorte@gmail.com", "dorte1234", "Dorte", None, False)]
    for s in init:
        add_user(conn, s[0], s[1], s[2], s[3], s[4], s[5])


def add_post(conn, post_id, title, image, body, tags, publish_date, admin_id):
    """
    Add a new post into the posts table
    :param conn:
    :param post id:
    :param title:
    :param image:
    :param body:
    :param tags:
    :param publish_date:
    :param admin_id:
    """
    sql = ''' INSERT INTO posts(post_id, title, image, body, tags, publish_date, admin_id)
              VALUES(?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (post_id, title, image, body, tags, publish_date, admin_id))
        conn.commit()
    except Error as e:
        print(e)

def init_posts(conn):
    init = [(1, "Halla folkens!", "fargegata.jpeg", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ultricies nisl a scelerisque tempor. Praesent risus tortor, elementum eu sodales non, pulvinar ut mi. Suspendisse quam mauris, imperdiet et ex vitae, auctor varius mi. Morbi non elit a nunc sodales efficitur. Donec enim magna, dignissim eu leo sed, placerat rutrum est. Nullam vel magna facilisis nisi accumsan pretium. Etiam elementum egestas enim, nec semper turpis cursus sit amet. Aenean vitae consequat tortor, et tristique ante", "hallo", "2024-05-07", 1),
            (2, "Hallo!", "Rosa_blogg.png", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ultricies nisl a scelerisque tempor. Praesent risus tortor, elementum eu sodales non, pulvinar ut mi. Suspendisse quam mauris, imperdiet et ex vitae, auctor varius mi. Morbi non elit a nunc sodales efficitur. Donec enim magna, dignissim eu leo sed, placerat rutrum est. Nullam vel magna facilisis nisi accumsan pretium. Etiam elementum egestas enim, nec semper turpis cursus sit amet. Aenean vitae consequat tortor, et tristique ante", "ingenting", "2024-05-10", 2),
            (3, "Vi er i Stavanger!", "preikestolen.jpeg", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ultricies nisl a scelerisque tempor. Praesent risus tortor, elementum eu sodales non, pulvinar ut mi. Suspendisse quam mauris, imperdiet et ex vitae, auctor varius mi. Morbi non elit a nunc sodales efficitur. Donec enim magna, dignissim eu leo sed, placerat rutrum est. Nullam vel magna facilisis nisi accumsan pretium. Etiam elementum egestas enim, nec semper turpis cursus sit amet. Aenean vitae consequat tortor, et tristique ante", "hei", "2024-05-20", 3)]
    for s in init:
        add_post(conn, s[0], s[1], s[2], s[3], s[4], s[5], s[6])


def add_subscription(conn, email, subscribed=True):
    """
    Add a new subscription into the subscriptions table
    :param conn:
    :param email:
    :param subscribed:
    """
    if not email:  # Sjekker om email er en tom streng
        raise ValueError("Du må oppgi en email")

    sql = ''' INSERT INTO subscriptions(email, subscribed)
              VALUES(?,?) '''
    try:
        cur = conn.cursor() 
        cur.execute(sql, (email, subscribed))
        conn.commit()
    except Error as e:
        print(e)


def init_subscriptions(conn):
    init = [("sofie@gmail.com", True),
            ("paulina@gmail.com", True),
            ("lisbeth@gmail.com", True), 
            ("anette@gmail.com", True)]
    for s in init:
        add_subscription(conn, s[0], s[1])


def setup():
    conn = create_connection(database)
    if conn is not None:
        delete_table(conn, "admins")
        delete_table(conn, "users")
        delete_table(conn, "posts")
        delete_table(conn, "subscriptions")
        create_table(conn, sql_create_admins_table)
        init_admins(conn)
        create_table(conn, sql_create_users_table)
        init_users(conn)
        create_table(conn, sql_create_posts_table)
        init_posts(conn)
        create_table(conn, sql_create_subscriptions_table)
        init_subscriptions(conn)
        conn.close()


if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()
