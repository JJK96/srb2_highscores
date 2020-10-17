from flask import Flask, send_file, send_from_directory
from api import api_routes, api_prefix
from map_voting import map_voting
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
app.register_blueprint(map_voting, url_prefix=map_voting_prefix)

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

# serve the svelte application if a path is not found
@app.errorhandler(404)
def page_not_found(e):
    return send_file('client/public/index.html')

# init the database connector
db.init_app(app)
migrate = Migrate(app, db)

# run
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
