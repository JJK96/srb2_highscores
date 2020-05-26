from flask_sqlalchemy import SQLAlchemy

# setup the database connector
db = SQLAlchemy()

# class for objects from the Map table
class Map(db.Model):
    __tablename__ = 'maps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '{{"id":"{}", "name":"{}"}}'.format(self.id, self.name)

# class for objects from the Highscore table
class Highscore(db.Model):
    __tablename__ = 'highscores'

    username = db.Column(db.String, primary_key=True)
    skin = db.Column(db.String, primary_key=True)
    map_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    time_string = db.Column(db.String)
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return "<Highscore {}, {}, {}, {}, {}, {}>".format(self.username,
                                                       self.skin, self.map_id,
                                                       self.time,
                                                       self.time_string,
                                                       self.datetime)

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
