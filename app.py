from flask import *

app = Flask(__name__, template_folder='Front_End/templates', static_folder='Front_End/static')
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





@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))  # redirects to index function above.




if __name__ == "__main__":
    app.run()

