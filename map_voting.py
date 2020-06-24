from flask import render_template, request, Blueprint
from database import db, Map, Voted
from config import Config

map_voting = Blueprint('map_voting', __name__)

@map_voting.route('/')
def list():
    query = db.session.query(Map).order_by(Map.votes.desc()).filter(Map.in_rotation)
    maps = query.all()
    return render_template('map_voting.html', maps=maps, config=Config)

@map_voting.route('/vote', methods = ['POST'])
def vote():
    map = int(request.form['map'])
    up = request.form['up'] == 'true'
    ip = request.remote_addr
    
    rowcount = db.session.query(
        Voted.ip,
        Voted.map) \
        .filter_by(ip=ip, map=map)
    
    if len(rowcount.all()) > 0:
        return "You have already voted on this map", 403

    db.session.query(Map.id,  Map.votes) \
        .filter_by(id=map) \
        .update({Map.votes: Map.votes + (1 if up else -1)}) 
    
    db.session.add(Voted(ip=ip, map=map))
    
    db.session.commit()
    return "thanks"
