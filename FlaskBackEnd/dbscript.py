import sqlite3

def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS USER("
              "username TEXT PRIMARY KEY,"
              "password TEXT NOT NULL,"
              "name TEXT,"
              "email TEXT,"
              "isAdmin INTEGER NOT NULL DEFAULT 0)")

    c.execute("CREATE TABLE IF NOT EXISTS EVENT("
              "eventID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "entryPrice INTEGER,"
              "name TEXT NOT NULL UNIQUE,"
              "timeDate TEXT,"
              "description TEXT,"
              "username TEXT,"  # taken from USER table.
              "FOREIGN KEY (username) REFERENCES USER(username))")  # username is FK from USER table.
    
    c.execute("CREATE TABLE IF NOT EXISTS SOCIETY("
              "societyID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "name TEXT NOT NULL UNIQUE)")
    
    c.execute("CREATE TABLE IF NOT EXISTS EVENTSOCIETY("
              "eventID INTEGER,"
              "societyID INTEGER,"
              "FOREIGN KEY (eventID) REFERENCES EVENT(eventID),"
              "FOREIGN KEY (societyID) REFERENCES SOCIETY(societyID),"
              "PRIMARY KEY (eventID, societyID))")
    conn.commit()
    conn.close()

def insertRecords(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO USER(username, password, name, email) VALUES (?,?,?,?)", ("Client1", "123","Berkay","berkay@gmail.com"))
    c.execute("INSERT INTO USER(username, password, name, email, isAdmin) VALUES (?,?,?,?,?)", ("Admin1", "123","Murat","murat@gmail.com",1))

    c.execute("INSERT INTO EVENT(entryPrice, name, timeDate, description, username) VALUES (?,?,?,?,?)",(50, "Tech Talk", "2025-05-10", "Technology conference", "Client1"))
    c.execute("INSERT INTO EVENT(entryPrice, name, timeDate, description, username) VALUES (?,?,?,?,?)",(30, "AI Workshop", "2025-06-01", "Hands-on AI session", "Client1"))

    c.execute("INSERT INTO SOCIETY(name) VALUES (?)",("Computer Society",))
    c.execute("INSERT INTO SOCIETY(name) VALUES (?)",("AI Society",))

    c.execute("INSERT INTO EVENTSOCIETY(eventID, societyID) VALUES (?,?)",(1, 1))
    c.execute("INSERT INTO EVENTSOCIETY(eventID, societyID) VALUES (?,?)",(1, 2))
    c.execute("INSERT INTO EVENTSOCIETY(eventID, societyID) VALUES (?,?)",(2, 2))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDatabase("school.db")
    insertRecords("school.db")