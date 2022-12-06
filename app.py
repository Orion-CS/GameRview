
# GameRview Semester Project
# R. Todd Pinsenschaum II, Andy Beichner, Amy Cunningham, Zach Goniea

from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy

# === Temp Data ===
from tempdata import mario_description

# === Forms ===
from registerForm import RegisterForm
from reviewForm import ReviewForm
from loginForm import LoginForm

# === Hasher ===
from hasher import Hasher

# === Login ===
from flask_login import UserMixin, current_user, login_user
from flask_login import LoginManager
login_manager = LoginManager()

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

# Identifying the Database File
dbfile = os.path.join(script_dir + "\database", "gamerview.sqlite3")


# Defining the Flask App
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'spiderweb'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Connect app to SQLite database
db = SQLAlchemy(app)

# Setup login
login_manager.init_app(app)

# region Database Models

# === Database Models ===
class VideoGame(db.Model):
    __tablename__ = 'VideoGames'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    releaseDate = db.Column(db.Unicode, nullable=False)
    studio = db.Column(db.Unicode, nullable=False)
    image = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode, nullable=False)
    trailerLink = db.Column(db.Unicode, nullable=True)
    rating = db.Column(db.Unicode, nullable=True)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)
    pwd_hash = db.Column(db.Unicode, nullable=False)

    def get(id_str):
        id_int = int(id_str)
        try:
            return User.query.filter_by(id=id_int).all()[0]
        except:
            return None

    def get_id(self):         
        return str(self.id)

class Friendship(db.Model):
    __tablename__ = 'Friendships'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Unicode, db.ForeignKey('Users.id'), nullable=False)
    friendId = db.Column(db.Unicode, db.ForeignKey('Users.id'), nullable=False)

class FavoritedGame(db.Model):
    __tablename__ = 'FavoritedGames'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Unicode, db.ForeignKey('Users.id'), nullable=False)
    gameId = db.Column(db.Unicode, db.ForeignKey('VideoGames.id'), nullable=False)

class Review(db.Model):
    __tablename__ = 'Reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Unicode, nullable=False)
    userId = db.Column(db.Unicode, db.ForeignKey('Users.id'), nullable=False)
    gameId = db.Column(db.Unicode, db.ForeignKey('VideoGames.id'), nullable=False)

# endregion

# region Helper Methods

def read_in_games():
    vg1 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description, trailerLink="https://www.youtube.com/embed/92bgHaM3B5A", rating="4/5")
    vg2 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description, trailerLink="https://www.youtube.com/embed/92bgHaM3B5A")
    vg3 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description, rating="4/5")
    vg4 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description)
    all_games = [vg1, vg2, vg3, vg4]
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
    db.drop_all() # TODO: remove this once get all actual data
    db.create_all()

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
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

#current_user = None


# === Routes ===
@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home/')
def home():
    all_games = VideoGame.query.all()

    # TODO:get the top games
    top_games = all_games
    return render_template("home_page.html", user=current_user, top_games=top_games)


@app.route('/register/', methods=["GET"])
def get_register():
    form = RegisterForm()
    return render_template("register_form.html", user=current_user, form=form)


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

@app.route('/review/<int:gId>/', methods=['GET'])
def get_review(gId):
    form = ReviewForm()
    return render_template("review_form.html", user=current_user, form=form, gId=gId)

@app.route('/review/<int:gId>/', methods=['POST'])
def post_review(gId):
    form = ReviewForm()
    if form.validate():
        # add the review to table
        text = form.review.data if form.review else ""
        rating = f"{form.rating.data}/5"
        r = Review(text=text, rating=rating, userId=current_user.id, gameId=gId)
        db.session.add(r)
        db.session.commit()
        return redirect(f"/game/{gId}")
    else:
        print("bruh")
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_review'))

@app.route('/game/<int:gId>/', methods=['GET'])
def get_game(gId):
    game = VideoGame.query.get_or_404(gId)
    reviews = Review.query.filter_by(gameId=game.id).all()
    reviewTups = []
    for review in reviews:
        user = User.query.filter_by(id=review.userId).all()[0]
        reviewTups.append((review, user))
    return render_template("game_page.html", user=current_user, game=game, reviewTups=reviewTups)

@app.route('/mygames/')
def get_my_games():
    if current_user.is_authenticated:
        favorite_games = []
        gameIds = FavoritedGame.query.filter_by(userId=current_user.id).all()
        for gId in gameIds:
            game = VideoGame.query.filter_by(id=gId).all()
            favorite_games.append(game)
        return render_template("mygames_page.html", user=current_user, favorite_games=favorite_games)
    return redirect(url_for('get_login'))   

@app.route('/friends/')
def get_friends():
    if current_user.is_authenticated:
        friendList = []
        friendIds = Friendship.query.filter_by(userId=current_user.id).all()
        for fId in friendIds:
            user = User.query.filter_by(id=fId).all()
            friendList.append(user)
        return render_template("friends_page.html", user=current_user, friendList=friendList)
    return redirect(url_for('get_login'))

@app.route('/calendarview/')
def get_calendar():
    return render_template("calendar_page.html", user=current_user)

@app.route('/profile/')
def get_profile():
    if current_user.is_authenticated:
        return render_template("profile_page.html", user=current_user)
    return redirect(url_for('get_login'))

@app.route('/login/', methods=['GET'])
def get_login():
    return render_template("login_page.html", user=current_user, form=LoginForm())

@app.route('/login/', methods=['POST'])
def post_login():
    form = LoginForm()
    if form.validate():
        users = User.query.all()
        for user in users:
            passEqual = hasher.check(pwd=form.password.data, pep_hash=user.pwd_hash)
            if user.email == form.credentials.data  or user.username == form.credentials.data and passEqual:
                # valid login
                login_user(user)
                #global current_user
                #current_user = user
                return redirect(url_for('get_profile'))
        flash("Invalid login")
        return redirect(url_for('get_login'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))
