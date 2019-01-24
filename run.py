import os
from flask import Flask, render_template, redirect, session, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone-project-4"
app.config["MONGO_URI"] = "mongodb://admin:cod4cmtmazza@ds161894.mlab.com:61894/milestone-project-4"

mongo = PyMongo(app)


def check_for_input(value):
    # If there was no input, return all results within that key by checking it exists.
    if value == False or value == "":
        return {"$exists": True}
    # If there was input, just return input.
    else:
        return value

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

@app.route("/log_out")
def log_out():
    # Remove user from session
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/filter", methods=["POST", "GET"])
def filter_home():
    """
        To filter through results, I will first declare that not all fields are required. I will then pass the input to the check_for_input() function
        There, it will find out if anything was filled in the fields. If the fields weren't filled in, I will just return all results within that key by checking it exists.
    """
    
    # Check if user is logged in
    logged_in = False
    if "username" in session:
        logged_in = True
    
    recipe_name = check_for_input(request.form["recipe_name"])
    country_of_origin = check_for_input(request.form.get("country_of_origin", False))
    category = check_for_input(request.form.get("category", False))
    allergens = check_for_input(request.form.get("allergens", False))
    tags = check_for_input(request.form.get("tags", False))
    
    # Query the database
    recipes = mongo.db.recipes.find({"recipe_name": recipe_name, "country_of_origin": country_of_origin, "category": category, "allergens": allergens, "tags": tags})
    # Get the amount of results
    count = recipes.count()
    return render_template("index.html", recipes = recipes, logged_in = logged_in, count = count) 

@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    """
        This function will pass through the selected recipe. It will check if the user is logged in, icrease the views of the recipe and display the recipe.
    """
    
    # Check if user is logged in - must pass through so the option to add to cook book will be hidden from users who aren't logged in
    logged_in = False
    if "username" in session:
        logged_in = True
        
    # The following lines of code will increase the views of the recipe and query the database. 
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    new_views = recipe["views"]
    new_views = new_views + 1
    mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, {"$set": {"views": new_views}})
    
    return render_template("view-recipe.html", recipe = recipe, logged_in = logged_in)

@app.route("/my_recipes")
def my_recipes():
    """
        Users can view the recipes they've created through this function. 
    """
    recipes = mongo.db.recipes.find({"author": session["username"]})
    count = recipes.count()
    
    return render_template("my-recipes.html", recipes = recipes, count = count)



@app.route("/create_recipe")
def create_recipe():
    """
        Users can create a recipe through this function.
    """
    return render_template("create-recipe.html", categories = mongo.db.categories.find())

@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    """
        Because of the complexity of my html form, I cannot use to_dict(), I also need to add author, views and upvotes which could not have been done in the form.
        To insert the list of ingredients / instructions, I needed to append them to a list. This is done with a loop. I have named the inputs with a loop in jQuery also.
        
        I will have to change the way allergens and tags are added to the database when I allow users to choose multiple options.
    """
    recipes = mongo.db.recipes
    author = session["username"]
    ingredients = []
    instructions = []
    find_category = mongo.db.categories.find({"category_name": request.form["category"]})
    number_of_ingredients = int(request.form["number_of_ingredients"])
    number_of_instructions = int(request.form["number_of_instructions"])
    
    # If user has decided to add their own category, I will check if it exists, then add to database.
    if find_category.count() == 0:
        mongo.db.categories.insert_one({"category_name": request.form["category"].lower().title()})
   
    for i in range(number_of_ingredients):
        # First letter of each ingredient will be uppercase.
        ingredients.append(request.form["ingredients[" + str(i) + "]"].lower().capitalize())
    
    for i in range(number_of_instructions):
        instructions.append(request.form["instructions[" + str(i) + "]"].lower().capitalize())
        
    recipes.insert_one({"recipe_name": request.form["recipe_name"].lower().title(), "recipe_desc": request.form["recipe_desc"].lower().capitalize(), "ingredients": ingredients, 
                        "country_of_origin": request.form["country_of_origin"].lower().title(), "allergens": [request.form["allergens"]], 
                        "tags": [request.form["tags"].lower().title()], "author": author, "up_down_votes": 0, "views": 0, "category": request.form["category"]})
                        
    return redirect(url_for("my_recipes"))




if __name__ == "__main__":
    app.secret_key = "$my$secret$key"
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
