from flask_sqlalchemy import SQLAlchemy

# setup the database connector
db = SQLAlchemy()

# class for objects from the Map table
class Map(db.Model):
    __tablename__ = 'maps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.LargeBinary)
    votes = db.Column(db.Integer)

    def __repr__(self):
        return '{{"id":"{}", "name":"{}", "image":"{}", "vote":"{}"}}'.format(self.id, self.name, self.image, self.vote)

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

# class for objects from the voted table
class Voted(db.Model):
    __tablename__ = "voted"
    
    ip = db.Column(db.String, primary_key=True)
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
