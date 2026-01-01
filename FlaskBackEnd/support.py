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
    c.execute("SELECT 1 FROM USER WHERE username=?",(username,))
    exists = c.fetchone()
    conn.close()

    if exists:
         return True
    
    return False

def society_exists(name):
     conn = get_db_connection()
     c = conn.cursor()
     c.execute("SELECT 1 FROM SOCIETY WHERE name=?",(name,))
     exists = c.fetchone()
     conn.close()

     if exists:
          return True
     return False


def get_societies_with_event_count():
    conn = get_db_connection()
    c = conn.cursor()

    # LEFT JOIN: event'i yoksa bile society listelensin, count 0 gelsin
    c.execute(
        'SELECT s.name, COUNT(es.eventID) ' #Burda ne göstermek istiyoruz onları gösteriyorum
        'FROM SOCIETY s LEFT JOIN EVENTSOCIETY es ' #Tüm societleri göster. societilerle EVENTSOCIETY’yi eşleştiriyorum Society varsa → her zaman listede Event’i yoksa → yine listede Sadece sağ taraf (EVENTSOCIETY) boş kalabilir
        'ON s.societyID = es.societyID ' #Aynı ID’ye sahip olanları eşleştir.
        'GROUP BY s.societyID, s.name ' #“Aynı society’ye ait olanları tek satırda topla.
        'ORDER BY s.name'#En son da alfabetik sıraya diz.
    )
    societies  = c.fetchall()
    conn.close()
    return societies 
