from flask import *
from support import *

app = Flask(__name__, template_folder='../Front_End/templates', static_folder='../Front_End/static')
app.secret_key = "123"

events = []

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

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
        c.execute("SELECT * FROM EVENT e, USER u WHERE e.username = u.username")
        events = c.fetchall()
        conn.close()
        return render_template("events.html",events = events)

    else:
        return redirect(url_for("index"))


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
        response = "Username has already been taken!"
    return response

if __name__ == "__main__":
    app.run()
    

