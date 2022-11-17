
# GameRview Semester Project
# R. Todd Pinsenschaum II, Andy Beichner, Amy Cunningham, Zach Goniea

from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy

# === Forms ===
from registerForm import RegisterForm
from reviewForm import ReviewForm
from loginForm import LoginForm

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

# region Database Models

# === Database Models ===
class VideoGame(db.Model):
    __tablename__ = 'Video Games'
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

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)

# endregion

# region Helper Methods

def read_in_games():
    all_games = []
    # read in games
    return all_games


def read_in_users():
    all_users = []
    # read in users
    return all_users

# endregion

def write_out_pepper(pepper_out):
    print("pepper_out:", pepper_out)
    pepper_file = open("pepper.txt", "w")
    pepper_file.write(pepper_out.decode('utf-8'))
    pepper_file.flush()
    pepper_file.close()


def read_in_pepper():
    pepper_file = open("pepper.txt", "r")
    my_pepper = pepper_file.readline()
    pepper_file.close()
    return my_pepper


# === Set Up Database ===
with app.app_context():
    # Create the database for this model
    db.drop_all()
    db.create_all()

    #db.session.add(Movie(title="The Fellowship of the Ring", year=2001, budget=93000000.0))
    db.session.add_all(read_in_games())
    db.session.add_all(read_in_users())
    db.session.commit()


# === Hashing ===
#pepper_out = Hasher.random_pepper()
#write_out_pepper(pepper_out=pepper_out)
pepper = read_in_pepper()
#print("pepper", pepper)
hasher = Hasher(bytes(pepper, encoding='utf-8'))

# === User ===
current_user = None


# === Routes ===
@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home/')
def home():
    return render_template("home_page.html", user=current_user)


@app.route('/register/', methods=["GET"])
def get_register():
    form = RegisterForm()
    return render_template("register_form.html", form=form)


@app.route('/register/', methods=["POST"])
def post_register():
    form = RegisterForm()
    if form.validate():
        users = User.query.all()
        for user in users:
            if user.username == form.username.data or user.email == form.email.data:
                # error not flashing 
                flash("Username or email already taken")
                return redirect(url_for('get_register'))

        # hash password
        pwd_hash = hasher.hash(form.password.data)
        userVar = User(username=form.username.data, email=form.email.data, pwd_hash=pwd_hash)
        #global current_user
        #current_user = userVar
        db.session.add(userVar)
        db.session.commit()
        return redirect(url_for('get_profile'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))

@app.route('/review/', methods=['GET'])
def get_review():
    form = ReviewForm()
    return render_template("review_form.html", form=form)

@app.route('/review/', methods=['POST'])
def post_review():
    form = ReviewForm()
    if form.validate():
        return redirect(url_for('get_review'))
    else:
        print("bruh")
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_review'))

@app.route('/game/', methods=['GET'])
def get_games():
    return render_template("game_page.html")

@app.route('/mygames/')
def get_my_games():
    return render_template("mygames_page.html")

@app.route('/friends/')
def get_friends():
    return render_template("friends_page.html")

@app.route('/calendarview/')
def get_calendar():
    return render_template("calendar_page.html")

@app.route('/profile/')
def get_profile():
    print(current_user != None)
    if current_user:
        return render_template("profile_page.html")
    return redirect(url_for('get_login'))

@app.route('/login/', methods=['GET'])
def get_login():
    return render_template("login_page.html", form=LoginForm())

@app.route('/login/', methods=['POST'])
def post_login():
    form = LoginForm()
    if form.validate():
        users = User.query.all()
        for user in users:
            passEqual = hasher.check(pwd=form.password.data, pep_hash=user.pwd_hash)
            if user.email == form.email.data and passEqual:
                # valid login
                global current_user
                current_user = user
                return redirect(url_for('get_profile'))
        flash("Invalid login")
        return redirect(url_for('get_login'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))