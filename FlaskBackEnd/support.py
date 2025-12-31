import sqlite3

def get_db_connection():
        conn = sqlite3.connect("school.db")
        return conn


def check_user(username, password):  #LOGİN SAYFASI İÇİN
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM USER WHERE username=? AND password=?",(username, password))
    user = c.fetchone()
    conn.close()
    return user


def username_exists(username): #O usernameli adam var mı yok mu
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT 1 FROM USER WHERE username=?",(username,))
    exists = c.fetchone()
    conn.close()

    if exists:
         return True
    
    return False
