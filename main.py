import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_wtf.csrf import CSRFProtect

import user_management as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
CSRFProtect(app)


@app.route("/success.html", methods=["POST", "GET"])
def addFeedback():
    if "username" not in session:
        return redirect(url_for("home", msg="Please log in first."))

    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)

    dbHandler.listFeedback()
    return render_template("/success.html", state=True, value=session["username"])


@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return redirect(url_for("home", msg="Signup successful. Please log in."))

    return render_template("/signup.html", state=("username" in session))


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("home", msg="You have been logged out."))


@app.route("/index.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        msg = request.args.get("msg", "")
        return render_template("/index.html", msg=msg, state=("username" in session))

    username = request.form["username"]
    password = request.form["password"]
    isLoggedIn = dbHandler.retrieveUsers(username, password)
    if isLoggedIn:
        session["username"] = username
        dbHandler.listFeedback()
        return render_template("/success.html", value=username, state=True)

    return render_template(
        "/index.html", msg="Invalid username or password.", state=False
    )


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(host="0.0.0.0", port=5000)
