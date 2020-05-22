from flask import Flask, render_template
from api import *
from database import db, key_to_column
from settings import username, password, host, database

class Config:
    static_dir = "static"
    base_url = ""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
app.register_blueprint(api_routes, url_prefix=api_prefix)

db.init_app(app)

@app.route('/')
def central_hub():
    return render_template('index.html', config=Config)

@app.route('/bestformaps')
def highscores_map_skin():
    return render_template('best_for_maps.html',
                           highscores=get_highscores(),
                           maps=get_maps(),
                           config=Config)

@app.route('/search')
def home():
    return render_template('search.html',
                           maps=get_maps(),
                           columns=[x for x in key_to_column.keys()],
                           skins=get_skins(),
                           users=get_users(),
                           config=Config)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
