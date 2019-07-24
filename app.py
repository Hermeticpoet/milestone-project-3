import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = '9039e1a76014f85ad2fea4415a793bd8'
app.config["MONGO_DBNAME"] = 'recipesApp'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')


#  Mongo Database Variable

mongo = PyMongo(app)

# recipes = mongo.db.recipes
# cuisines = mongo.db.vegetarian
# meal_type = mongo.db.ingredients
# diet = mongo.db.diet
# allergens = mongo.db.allergens
# users = mongo.db.portion_sizes

#  Landing Home Page

@app.route("/")
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html", title="Home")
    
# All Recipes

@app.route("/recipes")
def recipes():
    recipes = mongo.db.recipes.find()
    return render_template('recipes.html', recipes=recipes)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    # Validate Form Entry
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!')
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@yahoo.com' and form.password.data == 'password':
            flash("You have been successfully logged in")
            return redirect(url_for('index'))
        else:
            flash("Login Failed, please check username & password")
    return render_template("login.html", title="Login", form=form)
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

