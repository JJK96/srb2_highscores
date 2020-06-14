from flask import Flask, render_template
from api import *
from map_voting import *
from highscores import *
from config import Config
from database import db, key_to_column
from settings import username, password, host, database

highscores_prefix="/highscores"
map_voting_prefix="/map_voting"

# setup the class as a Flask object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.register_blueprint(api_routes, url_prefix=highscores_prefix + api_prefix)
app.register_blueprint(highscores, url_prefix=highscores_prefix)
app.register_blueprint(map_voting, url_prefix=map_voting_prefix)

@app.route('/')
def central_hub():
    # show the main page
    return render_template('index.html', config=Config)

# init the database connector
db.init_app(app)

# run
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
