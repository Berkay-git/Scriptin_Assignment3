import sqlite3

def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE user("
              "username TEXT PRIMARY KEY,"
              "password TEXT,"
              "fullname TEXT,"
              "gender TEXT)")

    c.execute("CREATE TABLE post("
              "postid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "content TEXT,"
              "username TEXT,"
              "FOREIGN KEY (username) REFERENCES user(username))")

    conn.close()