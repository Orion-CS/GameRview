# GameRview Semester Project
# R. Todd Pinsenschaum II, Andy Beichner, Amy Cunningham, Zach Goniea

from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy

# === Forms ===
from registerForm import RegisterForm

# === Database Models ===
#from dbModels import Movie

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

# Identifying the Database File
dbfile = os.path.join(script_dir, "gamerview.sqlite3")

# Defining the Flask App
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'spiderweb'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect app to SQLite database
db = SQLAlchemy(app)


# === Helper Methods ===
def read_in_movies():
    all_movies = []
    # read in movies
    return all_movies


def read_in_users():
    all_users = []
    # read in users
    return all_users


# Set up database
with app.app_context():
    # Create the database for this model
    db.drop_all()
    db.create_all()

    #db.session.add(Movie(title="The Fellowship of the Ring", year=2001, budget=93000000.0))
    db.session.add_all(read_in_movies())
    db.session.add_all(read_in_users())
    db.session.commit()


# === Routes ===
@app.route('/')
def index():
    return "GameRview"

@app.route('/register/', methods=["GET"])
def get_register():
    form = RegisterForm()
    return render_template("register_form.html", form=form)

@app.route('/register/', methods=["POST"])
def post_register():
    form = RegisterForm()
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        session['username'] = username
        session['email'] = email
        session['password'] = password
        return redirect(url_for('get_register'))
    else: 
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))
