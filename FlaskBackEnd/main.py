from flask import *

app = Flask(__name__)
app.secret_key = "123"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login")
def loginscreen():
    return render_template("login.html")

@app.route("/register")
def registerscreen():
    return render_template("register.html")

if __name__ == "__main__":
    app.run()

