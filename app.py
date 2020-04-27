from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from settings import username, password, host, database

class Config:
    static_dir = "static"
    base_url = ""

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
db = SQLAlchemy(app)


class Map(db.Model):
    __tablename__ = 'maps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '{{"id":"{}, "name":"{}}}'.format(self.id, self.name)


class Highscore(db.Model):
    __tablename__ = 'highscores'

    username = db.Column(db.String, primary_key=True)
    skin = db.Column(db.String, primary_key=True)
    map_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    time_string = db.Column(db.String)

    def __repr__(self):
        return "<Highscore {}, {}, {}, {}, {}>".format(self.username,
                                                       self.skin, self.map_id,
                                                       self.time,
                                                       self.time_string)


key_to_column = {
    'username': Highscore.username,
    'mapname': Map.name,
    'map_id': Map.id,
    'skin': Highscore.skin
}


def to_json(s):
    return json.dumps([x._asdict() for x in s])


@app.route('/api')
def api():
    query = db.session.query(
        Highscore.username,
        Map.name.label("mapname"),
        Map.id.label("map_id"),
        Highscore.skin,
        Highscore.time,
        Highscore.time_string) \
        .filter(Map.id == Highscore.map_id) \
        .order_by(Highscore.time.asc())

    for key in request.args:
        if key in key_to_column:
            query = query.filter(key_to_column[key] == request.args.get(key))
    limit = request.args.get('limit')
    if limit:
        try:
            query = query.limit(int(limit))
        except ValueError:
            pass

    result = query.all()
    return to_json(result)


def get_maps():
    query = db.session.query(Map)
    return query.all()


@app.route('/api/maps')
def maps():
    return str(get_maps())


def get_highscores():
    best_map = db.session.query(
        db.func.min(Highscore.time).label("time"),
        Highscore.skin,
        Highscore.map_id) \
        .group_by(Highscore.skin,
                  Highscore.map_id).subquery()
    query = db.session.query(
        Map.id.label("map_id"),
        Map.name.label("mapname"),
        Highscore.skin,
        Highscore.username,
        Highscore.time,
        Highscore.time_string
    ).select_from(Map,
                  db.join(Highscore, best_map,
                          (Highscore.skin == best_map.c.skin) & \
                          (Highscore.map_id == best_map.c.map_id) & \
                          (Highscore.time == best_map.c.time))) \
        .filter(Map.id == Highscore.map_id)
    maps = {}
    for row in query.all():
        map = maps.get(row.map_id, {
            'name': row.mapname,
            'skins': []
        })
        map['skins'].append({
            'name': row.skin,
            'username': row.username,
            'time': row.time,
            'time_string': row.time_string
        })
        maps[row.map_id] = map
    return [x for x in maps.values()]


@app.route('/api/highscores')
def api_highscores():
    return str(get_highscores())


@app.route('/')
def highscores_map_skin():
    return render_template('index.html',
                           highscores=get_highscores(),
                           config=Config)


@app.route('/search')
def home():
    return render_template('search.html',
                           maps=get_maps(),
                           config=Config)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
