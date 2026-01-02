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

def society_exists(name):  #ADMİN KULLANIYOR BUNU
     conn = get_db_connection()
     c = conn.cursor()
     c.execute("SELECT 1 FROM SOCIETY WHERE name=?",(name,))
     exists = c.fetchone()
     conn.close()

     if exists:
          return True
     return False


def get_societies_with_event_count(): # ADMİN İÇİN
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

def get_user(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT username, password, name, email FROM USER WHERE username=?",(username,))
    user = c.fetchone()
    conn.close()
    return user

def get_event_by_id(eventID):  #home page için 
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        "SELECT name, timeDate, description, entryPrice "
        "FROM EVENT WHERE eventID=?",
        (eventID,)
    )

    event = c.fetchone()
    conn.close()
    return event


def get_event_societies(eventID): #See more da gözügenler için 
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        "SELECT s.name "
        "FROM SOCIETY s, EVENTSOCIETY es "
        "WHERE s.societyID = es.societyID "
        "AND es.eventID=?",
        (eventID,)
    )

    societies = c.fetchall()
    conn.close()
    return societies

def get_events_grouped_by_society():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        "SELECT s.name, e.eventID, e.name, e.description, e.entryPrice "
        "FROM SOCIETY s, EVENT e, EVENTSOCIETY es "
        "WHERE s.societyID = es.societyID "
        "AND e.eventID = es.eventID "
        "ORDER BY s.name, e.name"
    )

    #SELECTTEN DOLAYI
    #row[0] → Society adı
    #row[1] → Event ID
    #row[2] → Event adı (Title)
    #row[3] → Event description
    #row[4] → Entry price (Free / Paid)

    rows = c.fetchall()
    conn.close()

    grouped = {}

    for row in rows:
        society = row[0]
        if society not in grouped:
            grouped[society] = []
        
        if row[4] == "Free":
            event_type = "Free Event"
        else:
            event_type = "Paid Event"
             

        grouped[society].append((row[1], row[2], row[3], event_type))

    return grouped
#Değiştirmeden ön ceki hali 