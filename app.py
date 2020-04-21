from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, render_template
import json
from settings import username, password, host, database

static_dir="/static/srb2_highscores"

app = Flask(__name__)

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

Base = declarative_base()

class Map(Base):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return '{{"id":"{}, "name":"{}}}'.format(self.id, self.name)

class Highscore(Base):
    __tablename__ = 'highscores'

    username = Column(String, primary_key=True)
    skin = Column(String, primary_key=True)
    map_id = Column(Integer, primary_key=True)
    time = Column(Integer)
    time_string = Column(String)

    def __repr__(self):
        return "<Highscore {}, {}, {}, {}, {}>".format(self.username, self.skin, self.map_id, self.time, self.time_string)

Session = sessionmaker(bind=engine)

key_to_column = {
    'username': Highscore.username,
    'mapname': Map.name,
    'map_id': Map.id,
    'skin': Highscore.skin
}

@app.route('/api')
def api():
    session = Session()
    query = session.query(
        Highscore.username,
        Map.name.label("mapname"),
        Map.id.label("map_id"),
        Highscore.skin,
        Highscore.time_string) \
        .filter(Map.id == Highscore.map_id) \
        .order_by(Highscore.time.asc())

    for key in request.args:
        if key in key_to_column:
            query = query.filter(key_to_column[key] == request.args.get(key))

    try:
        result = query.all()
        return json.dumps([x._asdict() for x in result])

    finally:
        session.close()

def get_maps():
    session = Session()
    query = session.query(Map)
    try:
        return query.all()
    finally:
        session.close()

@app.route('/api/maps')
def maps():
    return str(get_maps())

@app.route('/')
def home():
    return render_template('index.html', maps=get_maps(), static_dir=static_dir)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')

