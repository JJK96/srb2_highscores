from flask import Flask, render_template
from api import api_routes, api_prefix
from map_voting import map_voting
from highscores import highscores
from config import Config
from database import db
from settings import username, password, host, database
from flask_migrate import Migrate

highscores_prefix="/highscores"
map_voting_prefix="/map_voting"

# setup the class as a Flask object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(api_routes, url_prefix=api_prefix)
app.register_blueprint(highscores, url_prefix=highscores_prefix)
app.register_blueprint(map_voting, url_prefix=map_voting_prefix)

@app.route('/')
def central_hub():
    # show the main page
    return render_template('index.html', config=Config)

@app.route('/server_info')
def server_info():
    return render_template('server_info.html', config=Config)

# init the database connector
db.init_app(app)
migrate = Migrate(app, db)

# run
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
