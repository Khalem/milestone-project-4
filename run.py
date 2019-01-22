import os
from flask import Flask, render_template, redirect, session, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone-project-4"
app.config["MONGO_URI"] = "mongodb://admin:cod4cmtmazza@ds161894.mlab.com:61894/milestone-project-4"

mongo = PyMongo(app)

@app.route("/")
def index():
    logged_in = False
    
    if "username" in session:
        logged_in = True
        
    return render_template("index.html", logged_in = logged_in)

@app.route("/register", methods=["POST"])
def register():
    existing_user = mongo.db.user.find_one({"username": request.form["username"]})
    if existing_user is None:
        mongo.db.user.insert({"username": request.form["username"], "password": request.form["password"], "favourites_id": [], "created_id": []})
        session["username"] = request.form["username"]
        return redirect(url_for("index"))
    else:
        return "Username already taken!"

@app.route("/log_in", methods=["POST"])
def log_in():
    existing_user = mongo.db.user.find_one({"username": request.form["username"]})
    if existing_user:
        if request.form["password"] == existing_user["password"]:
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
    else:
        return "Username/Password is incorrect"

if __name__ == "__main__":
    app.secret_key = "$my$secret$key"
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)