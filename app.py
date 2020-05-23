from flask import Flask, render_template
from api import *
from database import db, key_to_column
from settings import username, password, host, database

# config the site
class Config:
    static_dir = "static"
    base_url = ""

# setup the class as a Flask object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
app.register_blueprint(api_routes, url_prefix=api_prefix)

# init the database connector
db.init_app(app)

# when the route is /
@app.route('/')
def central_hub():
    # show the main page
    return render_template('index.html', config=Config)

# when the route is /bestformaps
@app.route('/bestformaps')
def highscores_map_skin():
    # show the best for maps page
    return render_template('best_for_maps.html',
                           highscores=get_map_highscores(),
                           config=Config)

# when the route is /search
@app.route('/search')
def home():
    # show the search page
    return render_template('search.html',
                           maps=get_maps(),
                           columns=[x for x in key_to_column.keys()],
                           skins=get_skins(),
                           users=get_users(),
                           config=Config)

# when the route is /bestskins
@app.route('/bestskins')
def best_skins():
    # show the best skins page
    return render_template('best_skins_or_users.html',
                           data=get_best_in_data(False),
                           table_head_param=["Skin", "Best Times"],
                           title="Skins ordered by number of best timed tracks",
                           config=Config)

# when the route is /leaderboard
@app.route('/leaderboard')
def best_users():
    # show the leaderboard page
    return render_template('best_skins_or_users.html',
                           data=get_best_in_data(True),
                           table_head_param=["Player", "Points"],
                           title="Players' leaderboard (following mario kart's scoring system)",
                           config=Config)


# run
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
