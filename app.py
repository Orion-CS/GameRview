# GameRview Semester Project
# R. Todd Pinsenschaum II, Andy Beichner, Amy Cunningham, Zach Goniea

from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy

# === Forms ===
from registerForm import RegisterForm

# === Hasher ===
from hasher import Hasher

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

# === Database Models ===
class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    studio = db.Column(db.Unicode, nullable=False)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)
    pwd_hash = db.Column(db.Unicode, nullable=False)


# === Helper Methods ===
def read_in_movies():
    all_movies = []
    # read in movies
    return all_movies


def read_in_users():
    all_users = []
    # read in users
    return all_users


# def write_out_pepper(pepper_out):
#     pass


# def read_in_pepper():
#     my_pepper = 0
#     return my_pepper


# === Set Up Database ===
with app.app_context():
    # Create the database for this model
    db.drop_all()
    db.create_all()

    #db.session.add(Movie(title="The Fellowship of the Ring", year=2001, budget=93000000.0))
    db.session.add_all(read_in_movies())
    db.session.add_all(read_in_users())
    db.session.commit()


# # === Hashing ===
# #pepper = Hasher.random_pepper()
# pepper = read_in_pepper()
# hasher = Hasher(bytes(pepper))


# === Routes ===
@app.route('/')
def index():
    return render_template("home_page.html")


@app.route('/register/', methods=["GET"])
def get_register():
    form = RegisterForm()
    return render_template("register_form.html", form=form)


@app.route('/register/', methods=["POST"])
def post_register():
    form = RegisterForm()
    if form.validate():
        user = User(username = form.username.data, email = form.email.data, pwd_hash = form.password.data)
        db.session.add(user)
        db.session.commit()
        #pwd_hash = hasher.hash(password)
        #db.session.add(User(username=username, email=email, pwd_hash=pwd_hash))
        #db.session.commit()
        return redirect(url_for('get_register'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))
