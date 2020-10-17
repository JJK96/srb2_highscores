from flask import Flask, render_template, Blueprint
from api import *
from config import Config

highscores = Blueprint('highscores', __name__)

# when the route is /
@highscores.route('/')
def central_hub():
    # show the main page
    return render_template('highscores.html', config=Config)

# when the route is /bestformaps
@highscores.route('/bestformaps')
def highscores_map_skin():
    # show the best for maps page
    return render_template('best_for_maps.html',
                           config=Config)

# when the route is /search
@highscores.route('/search')
def home():
    # show the search page
    return render_template('search.html',
                           maps=get_maps(in_rotation=False),
                           columns=[x for x in key_to_column.keys()],
                           skins=get_skins(),
                           users=get_users(),
                           config=Config)

# when the route is /bestskins
@highscores.route('/bestskins')
def best_skins():
    # show the best skins page
    return render_template('best_skins.html',
                           config=Config)

# when the route is /leaderboard
@highscores.route('/leaderboard')
def best_users():
    # show the leaderboard page
    return render_template('leaderboard.html',
                           config=Config)
