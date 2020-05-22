from database import db, Map, Highscore, key_to_column
from flask import Blueprint, request, Response
from dataclasses import dataclass, field
import json

api_prefix = "/api"
api_routes = Blueprint('api', __name__)

@dataclass
class GetParam:
    param: str
    description: str
    values: list = None

@dataclass
class Endpoint:
    url: str
    description: str
    get_params: list = field(default_factory=list)

def to_json(s):
    return json.dumps([x._asdict() for x in s], default=lambda o: str(o))

def get_users():
    users = db.session.query(Highscore.username).distinct().all()
    return [x.username for x in users]

def get_skins():
    skins = db.session.query(Highscore.skin).distinct().all()
    return [x.skin for x in skins]

def get_maps():
    query = db.session.query(Map)
    return query.all()

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
        Highscore.time_string,
        Highscore.datetime
    ).select_from(Map,
                  db.join(Highscore, best_map,
                          (Highscore.skin == best_map.c.skin) & \
                          (Highscore.map_id == best_map.c.map_id) & \
                          (Highscore.time == best_map.c.time))) \
        .filter(Map.id == Highscore.map_id) \
        .order_by(Map.id, Highscore.time.asc())
    maps = {}
    for row in query.all():
        map = maps.get(row.map_id, {
            'id': row.map_id,
            'name': row.mapname,
            'skins': []
        })
        map['skins'].append({
            'name': row.skin,
            'username': row.username,
            'time': row.time,
            'time_string': row.time_string,
            'datetime': row.datetime
        })
        maps[row.map_id] = map
    return [x for x in maps.values()]

@api_routes.route('/')
def api():
    endpoints = [
        Endpoint(f'{api_prefix}/maps', 'Return all maps'),
        Endpoint(f'{api_prefix}/search', 'Return highscores ordered by time ascending', [
            GetParam('username', 'Search by username'),
            GetParam('mapname', 'Search by map name'),
            GetParam('map_id', 'Search by map id'),
            GetParam('skin', 'Search by skin', values=get_skins()),
            GetParam('limit', 'Set the maximal number of records to return'),
            GetParam('order', 'Order by any of the returned columns', values=[x for x in key_to_column.keys()]),
            GetParam('descending', 'Set the order direction to descending')
        ]),
        Endpoint(f'{api_prefix}/highscores', 'Get best scores per map and skin'),
        Endpoint(f'{api_prefix}/skins', 'Get the different skins in the database'),
        Endpoint(f'{api_prefix}/users', 'Get the different users in the database'),
    ]
    response = json.dumps({
        'endpoints': endpoints
    }, default=lambda o: o.__dict__)
    resp = Response(response=response, status=200, mimetype="application/json")
    return resp

@api_routes.route('/maps')
def maps():
    resp = Response(response=str(get_maps()), status=200, mimetype="application/json")
    return resp

@api_routes.route('/users')
def api_users():
    resp = Response(response=json.dumps(get_users()), status=200, mimetype="application/json")
    return resp

@api_routes.route('/skins')
def api_skins():
    resp = Response(response=json.dumps(get_skins()), status=200, mimetype="application/json")
    return resp

@api_routes.route('/highscores')
def api_highscores():
    resp = Response(response=json.dumps(get_highscores(), default=lambda o: str(o)), status=200, mimetype="application/json")
    return resp

@api_routes.route('/search')
def search():
    query = db.session.query(
        Highscore.username,
        Map.name.label("mapname"),
        Map.id.label("map_id"),
        Highscore.skin,
        Highscore.time,
        Highscore.time_string,
        Highscore.datetime) \
        .filter(Map.id == Highscore.map_id)
    
    order = request.args.get('order')
    descending = request.args.get('descending')
    if order in key_to_column:
        order_by = key_to_column[order]
        if descending:
            order_by = order_by.desc()
        query = query.order_by(order_by)
    query = query.order_by(Highscore.time.asc())

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
    resp = Response(response=to_json(result), status=200, mimetype="application/json")
    return resp
