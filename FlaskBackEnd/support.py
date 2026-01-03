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


def get_societies_with_event_count(): # for admin
    conn = get_db_connection()
    c = conn.cursor()

    # LEFT JOIN: even if it doesnt have event, list the society, make count 0
    c.execute(
        'SELECT s.name, COUNT(es.eventID) ' # write here what we need to show.
        'FROM SOCIETY s LEFT JOIN EVENTSOCIETY es ' #Tüm societleri göster. (EVENTSOCIETY) may stay empty.
        'ON s.societyID = es.societyID ' # list those who have same ID's.
        'GROUP BY s.societyID, s.name ' # list those who have same society name.
        'ORDER BY s.name'# reorder in alphabetic order
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

def get_event_by_id(eventID):  #for home page
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


def get_event_societies(eventID): # for 'see more'
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

    # due to 'select'
    #row[0] → Society name
    #row[1] → Event ID
    #row[2] → Event name (Title)
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

def getSocieties():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT s.name FROM SOCIETY s")
    socNames = c.fetchall()
    conn.close()
    return socNames


def searchInDatabase(keyword, selectedSociety):
    conn = get_db_connection()
    c = conn.cursor()

    key = "%" + keyword + "%"  # having our keyword between '%' signs will help us to match 'feren' with 'conference' because % sign doesn't care what is after or before the keyword.

    if selectedSociety == "all": # if 'all societies' is selected, then we will query all events that match keyword.
        c.execute("SELECT s.name, e.eventID, e.name, e.description, e.entryPrice "
                  "FROM EVENT e, EVENTSOCIETY es, SOCIETY s "
                  "WHERE e.eventID = es.eventID "
                  "AND es.societyID = s.societyID "
                  "AND (e.name LIKE ? OR e.description LIKE ?)",(key, key))

    else: # if a specific society is selected, we will come to the else part. Here we will add one more condition. s.name must match with selected society.
        c.execute("SELECT s.name, e.eventID, e.name, e.description, e.entryPrice "
                  "FROM EVENT e, EVENTSOCIETY es, SOCIETY s "
                  "WHERE e.eventID = es.eventID "
                  "AND es.societyID = s.societyID "
                  "AND s.name = ? "
                  "AND (e.name LIKE ? OR e.description LIKE ?)",(selectedSociety, key, key))

    results = c.fetchall()  # get query result and close the connection.
    conn.close()


    grouped_events = {}  # create a dictionary to populate it and send it to front-end.


    if selectedSociety != "all":              # specifically if there is a certain society selected in combo box,
        grouped_events[selectedSociety] = []  # initialize the key value so that it shows up even though it is empty.

    for row in results: # assign each event detail to variables, for easy process.
        soc_name = row[0]
        event_id = row[1]
        event_name = row[2]
        event_desc = row[3]
        price = row[4]


        if price == 0 or price is None:
            event_type = "Free Event" # will be shown in front-end.
        else:
            event_type = "Paid Event"

        event_data = [event_id, event_name, event_desc, event_type] # this is the format front end expects. (id,name,description,type)


        if soc_name in grouped_events:
            grouped_events[soc_name].append(event_data) # if we have this society in dictionary, append event.
        else:
            grouped_events[soc_name] = [event_data]   # if we don't have this society in dictionary, create a new event.

    # finally send the dictionary back. at this point each society can have zero or multiple events assigned to them.
    return grouped_events