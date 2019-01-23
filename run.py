import os
from flask import Flask, render_template, redirect, session, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone-project-4"
app.config["MONGO_URI"] = "mongodb://admin:cod4cmtmazza@ds161894.mlab.com:61894/milestone-project-4"

mongo = PyMongo(app)


@app.route("/")
@app.route("/<new_recipes>")
def index(new_recipes=None):
    
    logged_in = False
    
    if "username" in session:
        logged_in = True
    
    # Query the database
    recipes = mongo.db.recipes.find()
    # Get the amount of results
    count = recipes.count()
    
    return render_template("index.html", logged_in = logged_in, recipes = recipes, new_recipes = new_recipes, count = count)

@app.route("/register", methods=["POST"])
def register():
    """
    This function will allow users to register for the site. Their details will be saved to database under the 'user' collection
    """
    existing_user = mongo.db.user.find_one({"username": request.form["username"]})
    if existing_user is None:
        mongo.db.user.insert({"username": request.form["username"], "password": request.form["password"], "favourites_id": [], "created_id": []})
        session["username"] = request.form["username"]
        return redirect(url_for("index"))
    else:
        return "Username already taken!"

@app.route("/log_in", methods=["POST"])
def log_in():
    """
    This function will check the database to see if the username exists, then will compare it to the password.
    """
    existing_user = mongo.db.user.find_one({"username": request.form["username"]})
    if existing_user:
        if request.form["password"] == existing_user["password"]:
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
        else: 
            return "Username/Password is incorrect"
    else:
        return "Username/Password is incorrect"

@app.route("/filter", methods=["POST", "GET"])
def filter_home():
    """
        To filter through results, I will first declare that not all fields are required. I will then pass the input to the check_for_input() function
        There, it will find out if anything was filled in the fields. If the fields weren't filled in, I will just return all results within that key by checking it exists.
    """
    recipe_name = check_for_input(request.form["recipe_name"])
    country_of_origin = check_for_input(request.form.get("country_of_origin", False))
    category = check_for_input(request.form.get("category", False))
    allergens = check_for_input(request.form.get("allergens", False))
    tags = check_for_input(request.form.get("tags", False))
    
    # Query the database
    recipes = mongo.db.recipes.find({"recipe_name": recipe_name, "country_of_origin": country_of_origin, "category": category, "allergens": allergens, "tags": tags})
    # Get the amount of results
    count = recipes.count()
    return render_template("index.html", recipes = recipes, logged_in = True, count = count) 


def check_for_input(value):
    # If there was no input, return all results within that key by checking it exists.
    if value == False or value == "":
        return {"$exists": True}
    # If there was input, just return input.
    else:
        return value

if __name__ == "__main__":
    app.secret_key = "$my$secret$key"
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
