from flask import *
from support import *

app = Flask(__name__, template_folder='../Front_End/templates', static_folder='../Front_End/static')
app.secret_key = "123"

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def loginscreen():
    if request.method == "POST":  # if method is post, it means form in login.html is submitted, check information.
        username = request.form["username"]
        password = request.form["password"]
        exist = check_user(username,password)
        if exist != None:
            session["username"] = username
            session["isAdmin"] = exist[4]

        return redirect(url_for("index"))

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
        
        if email.startswith("org-"):
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




@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))  # redirects to index function above.




if __name__ == "__main__":
    app.run()
    

