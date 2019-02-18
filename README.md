# Milestone Project 4
For my 4th Milestone Project, I was required to create a recipe website that allows users to sign up, create and edit recipes, up or down vote on recipes.
I created this site with HTML, CSS, JavaScript and Python along with multiple frameworks / libraries.

My site "Easy Recipes" delivers all that I was required to do, along with a virtual "cook book", where users can add recipes that they like for easy access.
As it was my first time working with databases, I wanted to ensure that the site was fully functional while being visual pleasing at the same time.

## UX
For the design of this website, I wanted to keep it as simple as possible as not to take focus off the recipes. Using "fresh" colours for the Call to Action buttons will not only 
make it easier for users to notice, but will instill the feeling of fresh food. The website is obviously for people who enjoy cooking or baking. So being able to search through recipes
with ease is a must.

**User Stories:**
* **As a user I want to** view recipes so that I can learn how to make them
* **As a user I want to** create an account or log in so that I can up or down vote on recipes.
* **As a user I want to** be able to upload and edit my recipes so that I can show people.
* **As a user I want to** be able to search through recipes so that I can access recipes faster.
* **As a user I want to** add other peoples recipes to my favourites so I can access my favourites with ease.

I have left both a .xd and .pdf file of my wireframe in my [cloud9 workspace](https://ide.c9.io/khalemc/milestone-project-4).

## Features
#### Existing Features
* **Sign Up Btn** - allows users to sign up or login by typing their username and password.
* **Recipe Cards** - gives users an idea of what the recipe is and is clickable to view the full recipe.
* **Search Bar** - allows users to quickly find the recipe they want by filling out a form.
* **Pagination Links** - users can navigate through recipes by clicking on the links.
* **Create/Edit Recipe Form** - users can create/edit recipe by filling out a form.
* **Add to Cook Book Btn** - allows users to add other users recipes to their virtual cook book.
* **Delete Btn** - lets users delete recipes wether it be their own or from their cook book.
* **Up/Down Vote Btn** - users can up or down vote a recipe by clicking on a thumbs up or down.

#### Features Left to Implement
* **More details in recipes** - After I finished I realised there were more details I could have added to the recipes to make it more precise if a user wanted to search for a recipe.
* **Profile Page** - Although not necessary for this project, I would've liked to have a profile page where you could see what other users liked or uploaded.

## Technologies Used
* **HTML**
* **CSS**
  * [Materialize](https://materializecss.com/) - used for layout of site and for the many components of the site(forms, modals, etc..).
  * [Font Awesome](https://fontawesome.com/) - used for the icons of the site.
* **JavaScript**
  * [jQuery](https://jquery.com/) - used to simplify DOM manipulation.
  * [Materialize](https://materializecss.com/) - used for components of the site.
* **Python**
  * [flask](http://flask.pocoo.org/) - used for essentially all of the backend and partially front end with [Jinja](http://jinja.pocoo.org/).
  * [flask-paginate](https://pythonhosted.org/Flask-paginate/) - used to handle most of the pagination.
  * [PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) - used to handle the MongoDB queries in Python.
* [mLab(MongoDB)](https://mlab.com/) - used to host the database.

## Testing
For testing I tested the website with automated tests and by manual tests.

**Automated Tests:**

For my automated tests, I tested 2 different functions inside my main python code.

1. **Check for Input:** I tested to see if putting in a certain value would return the correct value.
2. **Get Records:** I tested the length of the returned list to see if pagination worked as inteded.

**Manual Tests:**

For my manual tests, I tested all features to find any bugs, both logged in and as a guest.

**Forms:** I tested the sign up, log in, edit and create recipe forms. For all tests I tested putting in an empty value to check it wouldn't submit. I also tested that the form would work as inteded - it did.

**Search Bar:** to test the search bar, I went onto all pages that had it, then began testing each indivdual search parameter. Everything worked as intended.

**Up/Down Vote:** I tested the up vote system by firstly trying to vote when I wasn't logged in. As I wanted, a tip would appear to encourage the user to log in/ sign up. Testing it logged in worked fine.

**Action Buttons:** I tested action buttons (edit, add, delte) by simply just clicking on them and seeing if they worked, they did.

**Pagination:** To test pagination, I changed the code the return 1 recipe per page to see if it worked. It did, I changed it back to 6 after testing.

**Responsiveness:**

While testing the responsiveness of the site, I noticed that on mobile landscapes, the padding of the landing caused it to overlap with some of the content. I fixed this by adding an extra media query. I tested 
the site by using chrome developer tools and [Responsinator](https://www.responsinator.com/). Just to be safe I tested it on my phone as well, I was pleased with the results.

## Changes I Would Like to Make
While I am proud of my work, there are a few changes that I would have liked to make but would have taken too much time this far into development. My biggest concern was the way I filtered through search results. Because I used flask-paginate,
I had to pass the entire query into the site address as a variable. This was necessary because if I used a __*request.method == "POST"*__ in the backend, I would lose any filtering the user had done once they would click on page 2/etc. I understand
that this wasn't the correct way of doing it, and in the future I will be sure to create my own pagination to avoid this problem.

## Deployment
I deployed the site onto **Heroku**. I did this by first creating a Procfile and a requirements.txt file. At first the requirements didn't include PyMongo because I used pip3 freeze, rather than pip freeze. 
I then created a secret key by revealing the config vars in settings. Once everything was in order, I pushed to Heroku and everything worked out fine. You can view the deployed site [here!](https://khalem-milestone-4.herokuapp.com/)

To run this code locally, I use Visual Studio 2017/ Port 5000.


## Credits
**Country Select:** To save a lot of time, I used some code provided by Github user asha23, you can view the source [here!](https://gist.github.com/asha23/6112572)

**Landing Photo:** I got the landing photo from [here!](https://www.pexels.com/photo/spinach-chicken-pomegranate-salad-5938/)

**Recipe Photos:** For recipe placeholder photos, I used [Pexels](https://www.pexels.com/), this site gives you a license to use all their photos for both commercial and personal use.