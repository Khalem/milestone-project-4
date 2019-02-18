import os
from flask import Flask, render_template, redirect, session, request, url_for, Blueprint
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_parameter
from bson.objectid import ObjectId
import ast

app = Flask(__name__)
app.secret_key = os.getenv("SECRETKEY", "randomstring123")

app.config["MONGO_DBNAME"] = "milestone-project-4"
app.config["MONGO_URI"] = "mongodb://admin:helloworld123@ds161894.mlab.com:61894/milestone-project-4"

mongo = PyMongo(app)

def check_for_input(value):
    # If there was no input, return all results within that key by checking it exists.
    if value == False or value == "" or value == []:
        return {"$exists": True}
    #  If user has selected multiple options, this will return the correct syntax for the mongodb query.
    elif type(value) == list and value:
        return {"$in": value}
    # If there was input, just return input.
    else:
        return value

def get_records(find_recipes, page_size, page_num):
        """
            This function will retrieve the correct recipes for pagination.
        """
        
        # Calculate number of documents to skip
        skips = page_size * (page_num - 1)

        # Skip and limit
        recipe = find_recipes.skip(skips).limit(page_size)

        # Return documents
        return [x for x in recipe]

@app.route("/")
@app.route("/<query>/<sort>")
def index(query = None, sort = None):
    categories = mongo.db.categories.find()
    tags = mongo.db.tags.find()
    allergens = mongo.db.allergens.find()
    
    
    if query == None:
        # If value of query doesn't change, return all reslults as user has just visited the site.
        recipes = mongo.db.recipes.find()
    else:
        # Convert query to dict by first changing it from unicode to str, then to dict using ast.literal_eval()
        # Use variable in the find query.
        query = str(query)
        dict_query = ast.literal_eval(query)
        recipes = mongo.db.recipes.find(dict_query)
    
    # These lines of code will sort the recipes depending on what the user picks.
    if sort == "most_views":
        recipes.sort([("views", -1)])
    elif sort == "least_views":
        recipes.sort([("views", 1)])
    elif sort == "best_rated":
        recipes.sort([("up_down_votes", -1)])
    elif sort == "worst_rated":
        recipes.sort([("up_down_votes", 1)])
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    # Get the amount of results
    count = recipes.count()
    
    # Pagination using flask-paginate
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page= 6, total=count, search=search, record_name="recipes")
    
    return render_template("index.html", recipes = get_records(recipes, 6, request.args.get(get_page_parameter(), type=int, default=1)),
                            count = count, pagination = pagination, sort = sort, query = query, categories = categories, tags = tags, allergens = allergens)


@app.route("/register", methods=["POST"])
def register():
    """
    This function will allow users to register for the site. Their details will be saved to database under the 'user' collection
    """
    existing_user = mongo.db.user.find_one({"username": request.form["username"]})
    if existing_user is None:
        mongo.db.user.insert({"username": request.form["username"], "password": request.form["password"], "cook_book": [], "up_voted": [], "down_voted": []})
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


@app.route("/filter_home", methods=["POST"])
def filter_home():
    """
        To filter through results, I will first declare that not all fields are required. I will then pass the input to the check_for_input() function
        There, it will find out if anything was filled in the fields. If the fields weren't filled in, I will just return all results within that key by checking it exists.
    """
    
    recipe_name = check_for_input(request.form["recipe_name"])
    country_of_origin = check_for_input(request.form.get("country_of_origin", False))
    category = check_for_input(request.form.get("category", False))
    allergens = check_for_input(request.form.getlist("allergens"))
    tags = check_for_input(request.form.getlist("tags"))
    time = check_for_input(request.form.get("recipe_time", False))
    
    print("test")
    print(allergens)
    
    return redirect(url_for("index", query = {"recipe_name": recipe_name, "country_of_origin": country_of_origin, "category": category, "allergens": allergens, "tags": tags, "recipe_time": time}, sort = "None")) 


@app.route("/filter_my_recipes", methods=["POST"])
def filter_my_recipes():
    """
        To filter through results, I will first declare that not all fields are required. I will then pass the input to the check_for_input() function
        There, it will find out if anything was filled in the fields. If the fields weren't filled in, I will just return all results within that key by checking it exists.
    """
    
    recipe_name = check_for_input(request.form["recipe_name"])
    country_of_origin = check_for_input(request.form.get("country_of_origin", False))
    category = check_for_input(request.form.get("category", False))
    allergens = check_for_input(request.form.getlist("allergens"))
    tags = check_for_input(request.form.getlist("tags"))
    time = check_for_input(request.form.get("recipe_time", False))
    
    return redirect(url_for("my_recipes", query = {"recipe_name": recipe_name, "country_of_origin": country_of_origin, "category": category, "allergens": allergens, "tags": tags, "recipe_time": time, "author": session["username"]}, sort = "None")) 

@app.route("/filter_cook_book", methods=["POST"])
def filter_cook_book():
    recipe_name = check_for_input(request.form["recipe_name"])
    country_of_origin = check_for_input(request.form.get("country_of_origin", False))
    category = check_for_input(request.form.get("category", False))
    allergens = check_for_input(request.form.getlist("allergens"))
    tags = check_for_input(request.form.getlist("tags"))
    time = check_for_input(request.form.get("recipe_time", False))
    
    return redirect(url_for("cook_book", query = {"recipe_name": recipe_name, "country_of_origin": country_of_origin, "category": category, "allergens": allergens, "tags": tags, "recipe_time": time}, sort = "None"))

@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    """
        This function will pass through the selected recipe. It will check if the user is logged in, icrease the views of the recipe and display the recipe.
    """
    
    # Check if user is logged in - must pass through so the option to add to cook book will be hidden from users who aren't logged in, also check if user has recipe in cook book.
    is_in = False
    up_down_voted = ""
    if "username" in session:
        user = mongo.db.user.find_one({"username": session["username"]})
    
        if recipe_id in user["up_voted"]:
            up_down_voted = "Up"
        elif recipe_id in user["down_voted"]:
            up_down_voted = "Down"
    
        # Check if user has recipe in cook book already. If they do a different button will apear for them to remove it.
        cook_book = user["cook_book"]
        if recipe_id in cook_book:
            is_in = True
    
    
    
    # The following lines of code will increase the views of the recipe and update the database. 
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    new_views = recipe["views"]
    new_views = new_views + 1
    
    mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, {"$set": {"views": new_views}})
    
    return render_template("view-recipe.html", recipe = recipe, is_in = is_in, up_down_voted = up_down_voted)


@app.route("/my_recipes/<query>/<sort>")
def my_recipes(query = None, sort = None):
    """
        Users can view the recipes they've created through this function. 
    """
    total = mongo.db.recipes.find({"author": session["username"]}).count()
    categories = mongo.db.categories.find()
    tags = mongo.db.tags.find()
    allergens = mongo.db.allergens.find()
    
    if query == "None":
        # If value of query doesn't change, return all reslults as user has just visited the site.
        recipes = mongo.db.recipes.find({"author": session["username"]})
    else:
        # Convert query to dict by first changing it from unicode to str, then to dict using ast.literal_eval()
        # Use variable in the find query.
        query = str(query)
        dict_query = ast.literal_eval(query)
        recipes = mongo.db.recipes.find(dict_query)
    
    # These lines of code will sort the recipes depending on what the user picks.
    if sort == "most_views":
        recipes.sort([("views", -1)])
    elif sort == "least_views":
        recipes.sort([("views", 1)])
    elif sort == "best_rated":
        recipes.sort([("up_down_votes", -1)])
    elif sort == "worst_rated":
        recipes.sort([("up_down_votes", 1)])
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    count = recipes.count()
    
    # Pagination using flask-paginate
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page= 6, total=count, search=search, record_name="recipes")
    
    return render_template("my-recipes.html", recipes = get_records(recipes, 6, request.args.get(get_page_parameter(), type=int, default=1)),
                            count = count, pagination = pagination, total = total, sort = sort, query = query, categories = categories, tags = tags, allergens = allergens)


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
    # Declaring variables
    recipes = mongo.db.recipes
    author = session["username"]
    ingredients = []
    instructions = []
    allergens = request.form.getlist("allergens")
    tags = request.form.getlist("tags")
    
    # Get category object
    find_category = mongo.db.categories.find({"category_name": request.form["category"]})
    # Get amount of ingredients
    number_of_ingredients = int(request.form["number_of_ingredients"])
    # Get amount of instructions
    number_of_instructions = int(request.form["number_of_instructions"])
    
    # If user has decided to add their own category, I will check if it exists, then add to database.
    if find_category.count() == 0:
        mongo.db.categories.insert_one({"category_name": request.form["category"].lower().title()})
   
   # Append ingredients to list
    for i in range(number_of_ingredients):
        # First letter of each ingredient will be uppercase.
        ingredients.append(request.form["ingredients[" + str(i) + "]"].lower().capitalize())
        
    # Get amount of instructions
    for i in range(number_of_instructions):
        instructions.append(request.form["instructions[" + str(i) + "]"].lower().capitalize())
        
    recipes.insert_one({"recipe_name": request.form["recipe_name"].lower().title(), "recipe_desc": request.form["recipe_desc"].lower().capitalize(), "ingredients": ingredients,
                        "instructions": instructions, "country_of_origin": request.form["country_of_origin"].lower().title(), "allergens": allergens, 
                        "tags": tags, "author": author, "up_down_votes": 0, "views": 0, "category": request.form["category"],
                        "number_of_ingredients": number_of_ingredients, "number_of_instructions": number_of_instructions, "img_src": request.form["img_src"], "recipe_time": request.form["recipe_time"]})
                        
    return redirect(url_for("my_recipes", query = "None", sort = "None"))


@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find()
    tags = mongo.db.tags.find()
    allergens = mongo.db.allergens.find()
    
    return render_template("edit-recipe.html", recipe = recipe, categories = categories, tags = tags, allergens = allergens)
  
  
@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    """
        This function works similar to insert_recipe() with copied lines of code. However I had to find the recipe views and upvotes to pass through with the update. Redirect
        to my_recipes().
    """
    # Declaring variables to update.
    recipes = mongo.db.recipes
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    ingredients = []
    instructions = []
    allergens = request.form.getlist("allergens")
    tags = request.form.getlist("tags")
    views = recipe["views"]
    upvotes = recipe["up_down_votes"]
    
    # Get category object
    find_category = mongo.db.categories.find({"category_name": request.form["category"]})
    # Get amount of ingredients
    number_of_ingredients = int(request.form["number_of_ingredients"])
    # Get amount of instructions
    number_of_instructions = int(request.form["number_of_instructions"])
    
    # If user has decided to add their own category, I will check if it exists, then add to database.
    if find_category.count() == 0:
        mongo.db.categories.insert_one({"category_name": request.form["category"].lower().title()})
   
   # Append ingredients to list
    for i in range(number_of_ingredients):
        # First letter of each ingredient will be uppercase.
        ingredients.append(request.form["ingredients[" + str(i) + "]"].lower().capitalize())
    
    # Append instructions to list
    for i in range(number_of_instructions):
        instructions.append(request.form["instructions[" + str(i) + "]"].lower().capitalize())
    
    # Test
    print(request.form.getlist("allergens"))
    print(request.form.getlist("tags"))
    
    recipes.update({"_id": ObjectId(recipe_id)},
                    {
                        "recipe_name": request.form["recipe_name"],
                        "recipe_desc": request.form["recipe_desc"],
                        "country_of_origin": request.form["country_of_origin"],
                        "allergens": allergens,
                        "number_of_ingredients": request.form["number_of_ingredients"],
                        "number_of_instructions": request.form["number_of_instructions"],
                        "ingredients": ingredients,
                        "instructions": instructions,
                        "category": request.form["category"],
                        "tags": tags,
                        "img_src": request.form["img_src"],
                        "recipe_time": request.form["recipe_time"],
                        "author": session["username"],
                        "views": views,
                        "up_down_votes": upvotes
                        
                    })
    
    return redirect(url_for("my_recipes", query = "None", sort = "None"))


@app.route("/delete_recipe/<recipe_id>/<query>/<sort>")
def delete_recipe(recipe_id, query, sort):
    """
        This function will remove recipe from database and redirect to my_recipes()
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("my_recipes", query = query, sort = sort))


@app.route("/add_cook_book/<recipe_id>")
def add_cook_book(recipe_id):
    user = mongo.db.user.find_one({"username": session["username"]})
    user_id = user["_id"]
    
    mongo.db.user.update_one({"_id": ObjectId(user_id)},
                    {"$push":
                {   
                    "cook_book": recipe_id
                }})
    
    return redirect(url_for("cook_book", query = "None", sort = "None"))
    

@app.route("/cook_book/<query>/<sort>")
def cook_book(query = None, sort = None):
    categories = mongo.db.categories.find()
    tags = mongo.db.tags.find()
    allergens = mongo.db.allergens.find()
    
    user = mongo.db.user.find_one({"username": session["username"]})
    cook_book = user["cook_book"]
    total = len(cook_book)
    for i in range(len(cook_book)):
        cook_book[i] = ObjectId(cook_book[i])
    
    if query == "None" :
        # If value of query doesn't change, return all reslults as user has just visited the site.
        recipes = mongo.db.recipes.find({"_id": {"$in": cook_book}})
    else:
        # Convert query to dict by first changing it from unicode to str, then to dict using ast.literal_eval()
        # Use variable in the find query.
        # Add cook_book to dict to search recipe id's
        query = str(query)
        dict_query = ast.literal_eval(query)
        dict_query["_id"] = {"$in": cook_book}
        recipes = mongo.db.recipes.find(dict_query)
    
    # These lines of code will sort the recipes depending on what the user picks.
    if sort == "most_views":
        recipes.sort([("views", -1)])
    elif sort == "least_views":
        recipes.sort([("views", 1)])
    elif sort == "best_rated":
        recipes.sort([("up_down_votes", -1)])
    elif sort == "worst_rated":
        recipes.sort([("up_down_votes", 1)])
    
    
    count = recipes.count()
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    # Pagination using flask-paginate
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page= 6, total=count, search=search, record_name="recipes")
    
    return render_template("cook-book.html", recipes = get_records(recipes, 6, request.args.get(get_page_parameter(), type=int, default=1)),
                            count = count, total = total, pagination = pagination, sort = sort, query = query, categories = categories, tags = tags, allergens = allergens)


@app.route("/remove_cook_book/<recipe_id>")
def remove_cook_book(recipe_id):
    """
        Allow user to remove recipe from cook book by using a mongodb command that will remove recipe_id from list. Redirect to cook_book()
    """
    mongo.db.user.update_one({"username": session["username"]},
                         {"$pull":
                             {
                                 "cook_book": recipe_id
                             }
                         })
    
    return redirect(url_for("cook_book", query = "None", sort = "None"))
    

@app.route("/up_voted/<recipe_id>")
def up_voted(recipe_id):
    """
        This function will increase the up_down_votes by 1 while also adding recipe_id to the up_voted list, and removing it from the down_voted list incase the user previously
        voted down on this recipe.
    """
    user = mongo.db.user.find_one({"username": session["username"]})
    up_voted = user["up_voted"]
    down_voted = user["down_voted"]
    if recipe_id not in up_voted:
        if recipe_id not in down_voted:
            mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)},
                                        {"$inc":
                                            {
                                                "up_down_votes": 1
                                            }
                                        })
    
            mongo.db.user.update_one({"username": session["username"]},
                                        {"$push":
                                            {
                                                "up_voted": recipe_id
                                            },
                                        "$pull":
                                             {
                                                 "down_voted": recipe_id
                                             }
                                        }
                                        )
        else:
            mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)},
                                        {"$inc":
                                            {
                                                "up_down_votes": 2
                                            }
                                        })
    
            mongo.db.user.update_one({"username": session["username"]},
                                        {"$push":
                                            {
                                                "up_voted": recipe_id
                                            },
                                        "$pull":
                                             {
                                                 "down_voted": recipe_id
                                             }
                                        }
                                        )
    
    return redirect(url_for("view_recipe", recipe_id = recipe_id))

@app.route("/down_voted/<recipe_id>")
def down_voted(recipe_id):
    """
        This function works the same as up_voted() except it will decrease up_down_votes and adds recipe_id to down_voted, and removes it
        from up_voted
    """
    user = mongo.db.user.find_one({"username": session["username"]})
    down_voted = user["down_voted"]
    up_voted = user["up_voted"]
    if recipe_id not in down_voted:
        if recipe_id not in up_voted:
            mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)},
                                    {"$inc":
                                        {
                                            "up_down_votes": -1
                                        }
                                    })
        
            mongo.db.user.update_one({"username": session["username"]},
                                        {"$push":
                                            {
                                                "down_voted": recipe_id
                                            },
                                        "$pull":
                                             {
                                                 "up_voted": recipe_id
                                             }
                                        }
                                        )
        else:
            mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)},
                                    {"$inc":
                                        {
                                            "up_down_votes": -2
                                        }
                                    })
        
            mongo.db.user.update_one({"username": session["username"]},
                                        {"$push":
                                            {
                                                "down_voted": recipe_id
                                            },
                                        "$pull":
                                             {
                                                 "up_voted": recipe_id
                                             }
                                        }
                                        )
    
    return redirect(url_for("view_recipe", recipe_id = recipe_id))
    
    
@app.errorhandler(404)
def page_not_found(e):
    """
        This function will handle 404 errors
    """
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.secret_key = "SECRETKEY"
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=False)
