from flask import *
import sqlite3

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
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM USER WHERE username=? AND password=?", (username, password))
        row = c.fetchone()
        conn.close()
        if row != None:
            session["username"] = username

        return redirect(url_for("index"))

    else:  # if method is get, show login.html.
        return render_template("login.html")


@app.route("/register")
def registerscreen():
    return render_template("register.html")





@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))  # redirects to index function above.




if __name__ == "__main__":
    app.run()

