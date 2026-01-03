from flask import *
from support import *

app = Flask(__name__, template_folder='../Front_End/templates', static_folder='../Front_End/static')
app.secret_key = "123"

events = []

@app.route("/")
@app.route("/index")
def index():
    error_message = request.args.get("error")
    societies = get_events_grouped_by_society()
    socNames = getSocieties()

    return render_template("index.html", societies=societies, socNames = socNames, error = error_message)

@app.route("/search")
def search():
    keyword = request.args.get("search", "")  # get the keyword from front-end.

    selected_society = request.args.get("society_filter", "all") # get the selected society from front-end.


    searchedSocieties = searchInDatabase(keyword, selected_society) # this will take keyword and selection, then it will find corresponding societies

    socNames = getSocieties()  # take all society names for combo box as usual.

    return render_template("index.html", societies=searchedSocieties, socNames = socNames)




@app.route("/login", methods=["POST", "GET"])
def loginscreen():
    if request.method == "POST":  # if method is post, it means form in login.html is submitted, check information.
        username = request.form["username"]
        password = request.form["password"]
        exist = check_user(username,password) # check if username is in database
        if exist != None:
            session["username"] = username
            session["isAdmin"] = int(exist[4])
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password") #Kullancıya hatayı göstermeliyiz



    else:  # if method is get, show login.html.
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        email  = request.form["email"]

        if username_exists(username):
            return render_template("register.html",error="Username already exists")
        
        if email.startswith("org-"): #email org ile başlıyorsa ilerde bu değiştirilebilir tabi ki!
            isAdmin = 1
        else :
            isAdmin = 0

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO USER(username, password, name, email, isAdmin) VALUES (?,?,?,?,?)", (username, password,name,email,isAdmin))
        conn.commit()
        conn.close()
        return redirect(url_for("loginscreen"))
    return render_template("register.html")


@app.route("/events", methods=["POST","GET"])
def seeevents ():
    if "username" in session:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT e.name, e.timeDate, GROUP_CONCAT(s.name, ', '), e.description, e.entryPrice, e.username, e.eventID "
                  "FROM Event e, SOCIETY s, USER u, EVENTSOCIETY es "
                  "WHERE u.username = e.username "
                    "AND e.eventID = es.eventID "
                    "AND es.societyID = s.societyID "
                  "GROUP BY e.eventID")
        # event name, event time & date, society name(s), event description and event entry price will be used to print events one by one.
        # event username will be used to check if logged in user and event creater user is the same user or not.
        # event ID will be used to delete corresponding event when "Delete" button is clicked.

        userEvents = []
        allEvents = c.fetchall() # right now allEvents contains all events created by all users.
        for each in allEvents:   # iterate all events
            if each[5] == session["username"]:  # to show events based on logged in user, we check if logged in username and event.username in database matches.
                userEvents.append(each) # userEvents will contain events that specifically created by logged in user.

        c.execute("SELECT s.societyID, s.name FROM SOCIETY s")
        societies = c.fetchall() # send all society names for society checkbox options in events.html (and also IDs to find out which ones are clicked.)


        conn.close()
        return render_template("events.html",events = userEvents, societies=societies)

    else:
        error = "You need to Login to Create an Event!!!"
        return redirect(url_for("index", error=error))


@app.route("/addevent", methods=["POST"])
def addEvent():
    if "username" not in session:
        return redirect(url_for("index"))

    name = request.form["name"]
    timeDate = request.form["timeDate"]
    description = request.form["description"] # get values from the form.


    societies = request.form.getlist("societies")

    fee_type = request.form["fee"]  # can be either free or paid.
    if fee_type == "free":
        entry_price = 'Free'
    else:
        entry_price = request.form["entryPrice"]  # if type is paid, also get the price.

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT name FROM EVENT")
    event_names=c.fetchall()
    if name in event_names: # check if event already exists. If yes return with error message.
        return render_template('events.html' ,error="Event already exists!, try again...")

    # insert pulled data to the database.
    c.execute("INSERT INTO Event (name, timeDate, description, entryPrice, username) VALUES (?, ?, ?, ?, ?)",(name, timeDate, description, entry_price, session["username"]))

    currentID=c.lastrowid  # c.lastrowid gives the current ID of the event.

    for each in societies:  # insert event & society connections one by one.
        c.execute("INSERT INTO EventSociety (eventID, societyID) VALUES (?, ?)",(currentID, each))

    conn.commit()
    conn.close()
    msg = "Event added successfully!"
    return redirect(url_for('seeevents'))


@app.route("/delete_event", methods=["POST"])
def delete_event():
    if "username" not in session:
        return redirect(url_for("login")) # if not logged in, redirect to login.


    event_id = request.form["event_id"] # get eventID from the hidden field in events.html.

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("DELETE FROM EVENTSOCIETY WHERE eventID = ?", (event_id,)) # first delete event from EventSociety

    c.execute("DELETE FROM EVENT WHERE eventID = ? AND username = ?", (event_id, session["username"])) # next, delete event directly from EVENT table.
    # I made sure that only logged in user can delete his/her events by adding "username = ?" and providing session["username"]

    conn.commit() # save and close.
    conn.close()

    return redirect(url_for("seeevents")) # show the new page.



@app.route("/managesocieties", methods=["POST","GET"])
def managesocieties():
    if "username" in session and session.get("isAdmin") == 1:
        error = ""
        success = ""

        if request.method == "POST":
            society_name = request.form.get("society_name", "").strip()

            if society_name == "":
                error = "Society name cannot be empty!"
            elif society_exists(society_name):
                error = "Society already exists!"
            else:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("INSERT INTO SOCIETY(name) VALUES (?)", (society_name,))
                conn.commit()
                conn.close()
                success = "Society added successfully."

        societies = get_societies_with_event_count()
        return render_template("managesocieties.html", societies=societies, error=error, success=success)
    else:
        return redirect(url_for("index"))

@app.route("/profile", methods=["POST","GET"])
def profile():
    if "username" in session:
        error = ""
        success = ""

        if request.method == "POST": #Edit butonuna bastın
            password = request.form.get("password", "").strip()
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            if password == "" or name == "" or email == "":
                error = "All fields must be filled!"
            else:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("UPDATE USER SET password=?, name=?, email=? WHERE username=?",(password, name, email,session["username"])) #burda direkt username de yollanır ama güvenlik açığı olmasın diye 
                conn.commit()
                conn.close()
                success = "Profile updated successfully."
        user = get_user(session["username"]) #burda direkt username de yollanır ama güvenlik açığı olmasın diye 
        return render_template(
            "profile.html",
            user=user,
            error=error,
            success=success
        )


    else:
        return redirect(url_for("index"))


@app.route("/event/<int:eventID>")
def event_detail(eventID):
    event = get_event_by_id(eventID)

    if not event:
        return redirect(url_for("index"))

    societies = get_event_societies(eventID)

    return render_template(
        "event.html",
        event=event,
        societies=societies,
        show_navbar= False # Bu sayede artık eventte yuakrdakiler yok
    )


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))  # redirects to index function above.

#AJAX CHECK ROUTLER BURDA

@app.get("/checkusername/<username>")  #AJAX ENTEGRE OLDU  BURASI checkussername burda paramatere alıyor username olarak ve register.html de olay
def check(username):
    exist = username_exists(username)
    response = ""
    if exist:
        response = " Username has already been taken!"
    return response

if __name__ == "__main__":
    app.run()
    

