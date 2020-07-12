from flask_sqlalchemy import SQLAlchemy

# setup the database connector
db = SQLAlchemy()

# class for objects from the Map table
class Map(db.Model):
    __tablename__ = 'maps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String, default=None)
    votes = db.Column(db.Integer, default=0)
    in_rotation = db.Column(db.Integer, default=1)

    def get_dict(self):
        map = {}
        for x in ['id', 'name', 'image', 'votes', 'in_rotation']:
            map[x] = self.__dict__[x]
        return map

    def __repr__(self):
        return '{{"id":"{}", "name":"{}", "image":"{}", "votes":"{}", "in_rotation":"{}"}}'.format(
            self.id,
            self.name,
            self.image,
            self.votes,
            self.in_rotation)

# class for objects from the Highscore table
class Highscore(db.Model):
    __tablename__ = 'highscores'

    score_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    skin = db.Column(db.String)
    map_id = db.Column(db.Integer)
    time = db.Column(db.Integer)
    time_string = db.Column(db.String)
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return "<Highscore {}, {}, {}, {}, {}, {}>".format(self.username,
                                                           self.skin,
                                                           self.map_id,
                                                           self.time,
                                                           self.time_string,
                                                           self.datetime)

# class for objects from the voted table
class Voted(db.Model):
    __tablename__ = "voted"

    ip = db.Column(db.String(15), primary_key=True)
    map = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<Voted {}, {}>".format(self.ip, 
                                       self.map)

# keys for the columns of the Highscore table
key_to_column = {
    'username': Highscore.username,
    'mapname': Map.name,
    'map_id': Map.id,
    'skin': Highscore.skin,
    'time': Highscore.time,
    'time_string': Highscore.time_string,
    'datetime': Highscore.datetime
}

# list of the vanilla skins
base_skins = [
    "sonic",
    "tails",
    "knuckles",
    "fang",
    "amy",
    "metalsonic"
]
