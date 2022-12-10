
# GameRview Semester Project
# R. Todd Pinsenschaum II, Andy Beichner, Amy Cunningham, Zach Goniea

from flask import Flask, request, render_template, redirect, url_for, abort, session, jsonify
from flask import flash
import random
from flask_sqlalchemy import SQLAlchemy

# === Temp Data ===
from tempdata import mario_description
import json

# === Forms ===
from registerForm import RegisterForm
from reviewForm import ReviewForm
from loginForm import LoginForm
from gamesearchForm import GameSearchForm
from usersearchForm import UserSearchForm
from userForm import UserForm

# === Hasher ===
from hasher import Hasher

# === Login ===
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from flask_login import LoginManager
login_manager = LoginManager()

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

gameInfoFile = os.path.join(script_dir, "gameInfo.json")

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
    rating = db.Column(db.Integer, nullable=True)
    rating_count = db.Column(db.Integer, nullable=True)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    profilePic = db.Column(db.Unicode, nullable=False)
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
    gameInformation = open(gameInfoFile)
    data = json.load(gameInformation)
    all_games = []
    for game in data:
        id = game.get('id', -1)
        cover = game.get('cover', 00000)
        studio = game.get('created_at', "No Studio")
        release = game.get('first_release_date', 0000)
        name = game.get('name', "anonymous")
        rating = game.get('rating', 0.0)
        rating_count = game.get('rating_count', 0)
        summary = game.get('summary', "No summary available.")

        # change rating from 0-100 to 0-5
        changed_rating = (rating/100) * 5
    
        new_game = VideoGame(id=id, title=name, releaseDate=release, studio="N/A", image="marioFiller.png", description=summary, trailerLink="https://www.youtube.com/embed/92bgHaM3B5A", rating=changed_rating, rating_count=rating_count)
        all_games.append(new_game)
        
        #vg2 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description, trailerLink="https://www.youtube.com/embed/92bgHaM3B5A")
        #vg3 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description, rating="4/5")
        #vg4 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description)
        #vg5 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description)
        #vg6 = VideoGame(title="Super Mario Bros 3", releaseDate="10/23/88", studio="Nintendo", image="marioFiller.png", description=mario_description)
    # read in games
    gameInformation.close()
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
    gsf = GameSearchForm()
    all_games = VideoGame.query.all()

    # TODO:get the top games
    top_games = all_games
    new_games = all_games
    return render_template("home_page.html", current_user=current_user, gsf=gsf, top_games=top_games, new_games=new_games)


@app.route('/register/', methods=["GET"])
def get_register():
    form = RegisterForm()
    return render_template("register_form.html", current_user=current_user, form=form)


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

        # random user image
        profile_pics = ["\static\icons\Xbox_button_A.svg.png", "\static\icons\Xbox_button_B.svg.png",
                            "\static\icons\Xbox_button_X.svg.png","\static\icons\Xbox_button_Y.svg.png"]
        selected_pic = random.choice(profile_pics)

        userVar = User(profilePic= selected_pic, 
            username=form.username.data, 
            email=form.email.data, 
            pwd_hash=pwd_hash)

        db.session.add(userVar)
        db.session.commit()
        login_user(userVar)
        return redirect(url_for('home'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))

@login_required
@app.route('/review/<int:gId>/', methods=['GET'])
def get_review(gId):
    form = ReviewForm()
    return render_template("review_form.html", current_user=current_user, form=form, gId=gId)

@login_required
@app.route('/review/<int:gId>/', methods=['POST'])
def post_review(gId):
    form = ReviewForm()
    if form.validate():
        # add the review to table
        text = form.review.data if form.review else ""
        rating = int(form.rating.data)
        r = Review(text=text, rating=rating, userId=current_user.id, gameId=gId)

        # change rating
        game = VideoGame.query.filter_by(id=gId).all()[0]
        cur_rating = game.rating
        cur_count = game.rating_count

        new_count = cur_count + 1
        new_rating = cur_rating + ((rating - cur_rating)/new_count)

        game.rating = new_rating
        game.cur_count = new_count

        db.session.add(r)
        db.session.commit()
        return redirect(f"/game/{gId}")
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_review'))

@app.route('/game/<int:gId>/', methods=['GET'])
def get_game(gId):
    gsf = GameSearchForm()
    game = VideoGame.query.get_or_404(gId)
    reviews = Review.query.filter_by(gameId=game.id).all()
    reviewTups = []
    for review in reviews:
        user = User.query.filter_by(id=review.userId).all()[0]
        reviewTups.append((review, user)) 
    return render_template("game_page.html", current_user=current_user, game=game, reviewTups=reviewTups, gsf=gsf)

@login_required
@app.route('/mygames/')
def get_my_games():
    gsf = GameSearchForm()
    if current_user.is_authenticated:
        favorite_games = []
        gId = FavoritedGame.query.filter_by(userId=current_user.id).all()
        for g in gId:
            game = VideoGame.query.filter_by(id=g.gameId).all()
            favorite_games.append(game[0])

        return render_template("mygames_page.html", current_user=current_user, favorite_games=favorite_games, gsf=gsf)
    return redirect(url_for('get_login'))

@login_required
@app.route('/friends/')
def get_friends():
    usf = UserSearchForm()
    gsf = GameSearchForm()
    friendList = []
    friendId = Friendship.query.filter_by(userId=current_user.id).all()
    for friend in friendId:
        user = User.query.filter_by(id=friend.friendId).all()
        friendList.append(user[0])
    return render_template("friends_page.html", current_user=current_user, friendList=friendList, gsf=gsf, usf=usf)

@app.route('/user/<int:id>')
def get_user(id):
    if current_user.is_authenticated:

        # check if trying to see myself
        if current_user.id == id:
            return redirect(url_for('get_my_games'))

        gsf = GameSearchForm()
        users = User.query.filter_by(id=id).all()
        foundUser = users[0]
        if foundUser:
            favorite_games = []
            gId = FavoritedGame.query.filter_by(userId=foundUser.id).all()
            for g in gId:
                game = VideoGame.query.filter_by(id=g.gameId).all()
                favorite_games.append(game[0])

            return render_template("friendsinfo_page.html", current_user=current_user, favorite_games=favorite_games, foundUser=foundUser, gsf=gsf)
        else:
            # stay on same page
            return redirect(request.url)
    return redirect(url_for('get_login'))

@app.route('/login/', methods=['GET'])
def get_login():
    return render_template("login_page.html", current_user=current_user, form=LoginForm())

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
                return redirect(url_for('home'))
        flash("Invalid login")
        return redirect(url_for('get_login'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))

@login_required
@app.route('/logout/', methods=['GET'])
def get_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/gamesearchresults/', methods=['POST'])
def post_searchresults():
    gsf = GameSearchForm()
    if gsf.validate():
        data = gsf.searchText.data if gsf.searchText.data else "*"
        return redirect(url_for('get_searchresults', searchString=data))
    return redirect(url_for('home'))

@app.route('/gamesearchresults/<string:searchString>/', methods=['GET'])
def get_searchresults(searchString="*"):
    gsf = GameSearchForm()
    if searchString == "*":
        searchString = ""
    games = VideoGame.query.all()
    results = []

    for game in games:
        if searchString.lower() in game.title.lower():
            results.append(game)
    return render_template("searchresults_page.html", current_user=current_user, results=results, gsf=gsf)

@app.route('/usersearchresults/', methods=['POST'])
def post_usersearchresults():
    usf = UserSearchForm()
    if usf.validate():
        data = usf.searchText.data
        return redirect(url_for('get_usersearchresults', searchString=data))
    # stay on same page
    return redirect(request.url)

@app.route('/usersearchresults/<string:searchString>/', methods=['GET'])
def get_usersearchresults(searchString="*"):
    gsf = GameSearchForm()
    if searchString == "*":
        searchString = ""
    users = User.query.all()
    results = []

    for u in users:
        if searchString.lower() in u.username.lower() and u.username != current_user.username:
            results.append(u)
    return render_template("userresults_page.html", current_user=current_user, results=results, gsf=gsf)

@app.route('/update/<int:id>', methods=['GET'])
def get_update_user(id):
    form = UserForm()
    user_to_update = User.query.get_or_404(id)
    return render_template("edit_account.html", user_to_update=user_to_update, form=form)

@app.route('/update/<int:id>', methods=['POST'])
def post_update_user(id):
    form = UserForm()
    user_to_update = User.query.get_or_404(id)
    if form.validate():     
        if not form.username.data == "" and form.email.data == "":
            user_to_update.username = form.username.data
        elif not form.email.data == "" and form.username.data == "":
            user_to_update.email = form.email.data
        elif form.email.data == "" and form.username.data == "":
            flash("Please fill in one of the fields.")
            return redirect(url_for('get_update_user', id=id))
        else:
            user_to_update.username = form.username.data
            user_to_update.email = form.email.data
        try:
            db.session.commit()
            flash("Successfully updated credentials.")
            return redirect(url_for('home', user_to_update=current_user))
        except: 
            flash("Error in updating credentials.")
            return redirect(url_for('get_update_user', id=id))
    else:  
        return redirect(url_for('home', user_to_update=current_user))

@app.route('/toggleFavorite/', methods=['POST'])
def toggleFavorite():
    toggle_data = request.get_json()
    gameId = toggle_data[0].get("gameId")
    userId = current_user.id
    isFavorite = False

    favGames = FavoritedGame.query.filter_by(userId=userId, gameId=gameId).all()
    print(favGames)
    if favGames:
        # returned a game so remove it
        favGame = favGames[0]
        db.session.delete(favGame)
        db.session.commit()
    else:
        # returned nothing so add it
        newFGame = FavoritedGame(userId=userId, gameId=gameId)
        isFavorite = True
        db.session.add(newFGame)
        db.session.commit()

    results = {'favorite': isFavorite}
    return jsonify(results)

@app.route('/getFavorite/', methods=['POST'])
def getFavorite():
    toggle_data = request.get_json()
    gameId = toggle_data[0].get("gameId")
    userId = current_user.id
    isFavorite = False

    favGames = FavoritedGame.query.filter_by(userId=userId, gameId=gameId).all()
    
    if favGames:
        isFavorite = True

    results = {'favorite': isFavorite}
    return jsonify(results)

@app.route('/toggleFriend/', methods=['POST'])
def toggleFriend():
    toggle_data = request.get_json()
    friendId = toggle_data[0].get("friendId")
    userId = current_user.id
    isFriend = False

    friends = Friendship.query.filter_by(userId=userId, friendId=friendId).all()

    if friends:
        # returned a game so remove it
        friend = friends[0]
        db.session.delete(friend)
        db.session.commit()
    else:
        # returned nothing so add it
        friend = Friendship(userId=userId, friendId=friendId)
        isFriend = True
        db.session.add(friend)
        db.session.commit()

    results = {'friend': isFriend}
    return jsonify(results)

@app.route('/getFriend/', methods=['POST'])
def getFriend():
    toggle_data = request.get_json()
    friendId = toggle_data[0].get("friendId")
    userId = current_user.id
    isFriend = False

    favGames = Friendship.query.filter_by(userId=userId, friendId=friendId).all()
    
    if favGames:
        isFriend = True

    results = {'friend': isFriend}
    return jsonify(results)