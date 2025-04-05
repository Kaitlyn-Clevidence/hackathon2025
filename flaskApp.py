from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landingPage.html")

#make about available before signing in? or just make a lil about section in welcome page
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup/", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Placeholder: Add user to database here
        print(f"New user: {username}, {email}, {password}")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # handle login logic here
        return redirect(url_for("personalView"))
    return render_template("login.html")

#need user before calendar??
@app.route("/calendar/")
def calendar():
    return render_template("calendar.html")

@app.route("/tips/")
def tips():
    return render_template("tips.html")

@app.route("/wishlist/")
def wishlist():
    return render_template("wishlist.html")

@app.route("/budget/")
def budget():
    return render_template("budget.html")

@app.route("/logout/")
def logout():
    # session.clear()  # Uncomment if using session-based auth
    return redirect(url_for("landing"))

@app.route("/main/")
def personalView():
    return render_template("dashboard.html")

#@app.route("/<username>/")
#def personalView(username):
    #heres where we start referencing the database for their personal events and settings \
 #   pass

if __name__ == "__main__":
    app.run(debug=True)