from database import db, Map, Highscore, key_to_column, base_skins
from flask import Blueprint, request, Response, jsonify
from dataclasses import dataclass, field
import json
from json.decoder import JSONDecodeError
from collections import defaultdict
from srb2_query import SRB2Query, mapname_to_num
from config import Config
from fuzzywuzzy import process, fuzz
from werkzeug.exceptions import HTTPException
from sqlalchemy import func, and_

# setup the api section of the site
api_prefix = "/highscores/api"
api_routes = Blueprint('api', __name__)

# class for the api search parameters
@dataclass
class GetParam:
    param: str
    description: str
    values: list = None

# class for the api endpoints
@dataclass
class Endpoint:
    url: str
    description: str
    get_params: list = field(default_factory=list)


# convert a list to json
def to_json(s):
    return json.dumps([x._asdict() for x in s], default=lambda o: str(o))

# get all the users in the database
def get_users():
    users = db.session.query(Highscore.username).distinct().all()
    return [x.username for x in users]

# get all the skins in the database
def get_skins():
    skins = db.session.query(Highscore.skin).distinct().all()
    return [x.skin for x in skins]

# get all the maps in the database
# @param in_rotation: Only return maps that are in rotation
def get_maps(id=None, in_rotation=True, ordering=None):
    query = db.session.query(Map)
    if in_rotation:
        query = query.filter(Map.in_rotation)
    if ordering is not None:
        query = query.order_by(ordering)
    if id:
        query = query.filter(Map.id == id)
        return query.one_or_none()
    return query.all()

# get the best highscores for each skin in each map
def get_map_highscores(all_skins=False, map_id=None, start_date=None, end_date=None, **kwargs):
    # get the best time for each map and skin
    best_map = db.session.query(
        db.func.min(Highscore.time).label("time"),
        Highscore.skin,
        Highscore.map_id) \
        .group_by(Highscore.skin,
                  Highscore.map_id).subquery()
    # get all the highscores and select the scores from the found best scores
    query = db.session.query(
        Map.id.label("map_id"),
        Map.name.label("mapname"),
        Map.image,
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
        .filter(Map.in_rotation) \
        .order_by(Map.id, Highscore.time.asc())

    if not all_skins:
        query = query.filter(Highscore.skin.in_(base_skins))

    if map_id:
        query = query.filter(Highscore.map_id == map_id)

    if start_date is not None:
        query = query.filter(Highscore.datetime >= start_date)

    if end_date is not None:
        query = query.filter(Highscore.datetime <= end_date)

    maps = {}
    
    # for every score in the filtered scores
    for row in query.all():
        # save the scores
        map = maps.get(row.map_id, {
            'id': row.map_id,
            'name': row.mapname,
            'image': row.image,
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

# Gets the best skins in the database 
def get_best_skins(all_skins=False, limit=1, filters=None, **kwargs):
    scoring = defaultdict(int)
    if filters is None:
        filters = []

    # for every map in the highscores
    for map in get_maps():
        map_filters = [] + filters
        map_filters.append(Highscore.map_id == map.id)
        scores = search(filters=map_filters, **kwargs)
        if len(scores) > 0:
            scoring[scores[0].skin] += 1

    res = {}
    # sort the dictionary by most points
    for k, v in sorted(scoring.items(), key=lambda x: x[1], reverse=True):
        res[k] = v
    return res

# Gets the leaderboard of users in the database 
def get_leaderboard(include_calculation=False, username=None, skin=None, limit=11, filters=None, **kwargs):
    # setup the dictionaries for the storing of the results
    scoring = {}
    
    # setup the weights for the leaderboard(mariokart's scoring system)
    weights = {
        1:15,
        2:12,
        3:10,
        4:8,
        5:7,
        6:6,
        7:5,
        8:4,
        9:3,
        10:2,
        11:1
    }

    if filters is None:
        filters = []

    # for every map in the highscores
    for map in get_maps():
        map_filters = [] + filters
        map_filters.append(Highscore.map_id == map.id)
        if skin:
            map_filters.append(Highscore.skin == skin)
        scores = search(filters=map_filters, limit=limit, **kwargs)
        # for every score in the map's highscores
        for place, score in enumerate(scores):
            score_username = score.username
            if username and score_username != username:
                continue
            place = place+1
            # add increase the points in the dictionary by the username
            user = scoring.get(score_username, {
                'username': score_username,
                'total': 0
            })
            points = weights.get(place, 0)
            if include_calculation:
                score = score._asdict()
                score['place'] = place
                score['points'] = points
                if 'scores' not in user:
                    user['scores'] = []
                user['scores'].append(score)
            user['total'] += points
            scoring[score_username] = user
    # sort the dictionary by most points
    return sorted(scoring.values(), key=lambda x: x['total'], reverse=True)

# converter from tics to string
def tics_to_string(time):
    minutes = time//(60*35)
    seconds = time//35%60
    centiseconds = (time%35) * (100//35)
    return f"{minutes}:"+f"{seconds}".zfill(2)+f".{centiseconds}".zfill(2)


# Returns the maps with the number of times they were played since the given start_date
# 2020-09-10 was the date the ingame voting system was enabled
def get_num_plays(start_date="2020-09-10"):
    subquery = db.session.query(
        Highscore.map_id,
        Highscore.datetime) \
        .filter(Highscore.datetime > start_date) \
        .distinct() \
        .subquery()
    num_plays = func.count().label("num_plays")
    query = db.session.query(
        Map.id,
        Map.name,
        Map.image,
        num_plays) \
        .select_from(Map, subquery) \
        .filter(Map.id == subquery.c.map_id) \
        .group_by(subquery.c.map_id) \
        .order_by(num_plays.desc())
    return query.all()

# Returns how much records are set on specific days of the week, hours, etc.
def get_time_stats(day=True, hour=False):
    if not day and not hour:
        # This is not a useful query, transform it
        day = True
    columns = []
    if day:
        columns.append(func.dayname(Highscore.datetime).label("day"))
    if hour:
        columns.append(func.hour(Highscore.datetime).label("hour"))
    columns.append(func.count().label("num_scores"))

    query = db.session.query(*columns) \
        .filter(Highscore.datetime) \

    if day:
        query = query.group_by("day").order_by("day")
    if hour:
        query = query.group_by("hour").order_by("hour")

    output = {}
    for row in query.all():
        if day and hour:
            d = output.get(row.day, {})
            d[row.hour] = row.num_scores
            output[row.day] = d
        elif day:
            output[row.day] = row.num_scores
        elif hour:
            output[row.hour] = row.num_scores

    return output

fuzzy_columns = {'username':get_users, 'mapname':lambda:[map.name for map in get_maps(in_rotation=False)], 'skin':get_skins}
# if the column has to be searched through fuzzywuzzy

def get_fuzzy(key, value):
    try:
        extracted = process.extractOne(value, fuzzy_columns[key](), scorer=fuzz.ratio)
        return extracted[0]
    except KeyError:
        # filter the highscores by such column
        return value


# when the route is api/
@api_routes.route('/')
def api():
    # show the docs for every endpoint in the api section
    endpoints = [
        Endpoint(f'{api_prefix}/maps', 'Return all maps', [
            GetParam('in_rotation', 'Get only maps that are in the rotation'),
            GetParam('order', 'Order by any of the returned columns', values=Map.__table__.columns._data.keys()),
        ]),
        Endpoint(f'{api_prefix}/maps/<id>', 'Return the specified map'),
        Endpoint(f'{api_prefix}/maps/<mapname>', 'Return the map indicated by the mapname parameter e.g. MAPR0 or r0'),
        Endpoint(f'{api_prefix}/search', 'Return highscores ordered by time ascending. All get parameters can also be given as a json list of values e.g. map_id=[1,2]', [
            GetParam('username', 'Search by username'),
            GetParam('mapname', 'Search by map name'),
            GetParam('map_id', 'Search by map id'),
            GetParam('skin', 'Search by skin', values=get_skins()),
            GetParam('limit', 'Set the maximal number of records to return'),
            GetParam('order', 'Order by any of the returned columns', values=[x for x in key_to_column.keys()]),
            GetParam('descending', 'Set the order direction to descending'),
            GetParam('all_scores', 'Set to "on" to get all the scores instead of just the best ones'),
            GetParam('all_skins', 'Set to "on" to get all the skins instead of just the vanilla ones'),
            GetParam('per_skin', 'Set to "off" to get only one score per user per map'),
            GetParam('start_date', 'Return only scores after this date'),
            GetParam('end_date', 'Return only scores before this date'),
            GetParam('fuzzy', 'Set to "off" to disable fuzzy matching'),
        ]),
        Endpoint(f'{api_prefix}/skins', 'Get the different skins in the database'),
        Endpoint(f'{api_prefix}/users', 'Get the different users in the database'),
        Endpoint(f'{api_prefix}/leaderboard', 'Get the leaderboard of the best players', [
            GetParam('all_skins', 'Set to "on" to count points for the scores with all the skins instead of just the vanilla ones'),
            GetParam('per_skin', 'Set to "off" to get only one score per user per map'),
            GetParam('include_scores', 'Add this parameter to include all scores that contributed to the calculation'),
            GetParam('username', 'Get only the scores of the given username'),
            GetParam('skin', 'Get only scores for the given skin'),
            GetParam('start_date', 'Use only scores after this date'),
            GetParam('end_date', 'Use only scores before this date'),
        ]),
        Endpoint(f'{api_prefix}/bestskins', 'Get the best skins by number of best timed tracks without modded skins', [
            GetParam('all_skins', 'Set to "on" to count points for the scores with all the skins instead of just the vanilla ones'),
            GetParam('start_date', 'Use only scores after this date'),
            GetParam('end_date', 'Use only scores before this date'),
        ]),
        Endpoint(f'{api_prefix}/bestformaps', 'Get the highscores divided by map', [
            GetParam('map_id', 'Search by map id'),
            GetParam('start_date', 'Use only scores after this date'),
            GetParam('end_date', 'Use only scores before this date'),
        ]),
        Endpoint(f'{api_prefix}/server_info[/<ip_address>][/<port>]', 'Get info from the SRB2 server, optionally with the given ip_address and/or port instead of the default'),
        Endpoint(f'{api_prefix}/num_plays/[<start_date>]', 'Get the number of times each map was played since the given date'),
        Endpoint(f'{api_prefix}/time_stats', 'Get the number of records grouped based on the arguments', [
            GetParam('day', 'Group by day of the week'),
            GetParam('hour', 'Group by hour of the day'),
        ]),
    ]
    # return the docs as json
    response = json.dumps({
        'endpoints': endpoints
    }, default=lambda o: o.__dict__)
    resp = Response(response=response, status=200, mimetype="application/json")
    return resp

# when the route is api/maps
@api_routes.route('/maps')
@api_routes.route('/maps/<int:id>')
@api_routes.route('/maps/<mapname>')
def maps(id=None, mapname=None):
    in_rotation = request.args.get("in_rotation") is not None
    ordering = request.args.get("order")
    descending = 'descending' in request.args
    if mapname:
        # subtract 1 because we start at 0 instead of 1
        id = mapname_to_num(mapname)-1

    if ordering is not None:
        order_by = getattr(Map, ordering)
        if descending:
            # order in descending order
            order_by = order_by.desc()
        ordering = order_by

    maps = get_maps(id, in_rotation=in_rotation, ordering=ordering)
    if maps is None:
        return jsonify(error="Map not found"), 404
    else:
        # return the maps as json
        resp = Response(response=str(maps), status=200, mimetype="application/json")
        return resp

# when the route is api/users
@api_routes.route('/users')
def api_users():
    # return the users as json
    resp = Response(response=json.dumps(get_users()), status=200, mimetype="application/json")
    return resp

# when the route is api/skins
@api_routes.route('/skins')
def api_skins():
    # return the skins as json
    resp = Response(response=json.dumps(get_skins()), status=200, mimetype="application/json")
    return resp

# when the route is api/leaderboard
@api_routes.route('/leaderboard')
def api_leaderboard():
    # request the params for the skins to be counted
    search_params = parse_search_params()

    include_calculation = "include_calculation" in request.args
    username = request.args.get("username", None)
    skin = request.args.get("skin", None)
    if skin and skin not in base_skins:
        search_params['all_skins'] = True

    # return the leaderboard as json
    return jsonify(get_leaderboard(
        include_calculation=include_calculation,
        username=username,
        skin=skin,
        **search_params
    ))

# when the route is api/bestskins
@api_routes.route('/bestskins')
def api_best_skins():
    search_params = parse_search_params()
    
    # return the best skins as json
    resp = Response(response=json.dumps(get_best_skins(**search_params)), status=200, mimetype="application/json")
    return resp

# when the route is api/bestformaps
@api_routes.route('/bestformaps')
def api_highscores():
    search_params = parse_search_params()
    map_id = request.args.get("map_id")
    # return the highscores for each skin in each map as json
    resp = Response(response=json.dumps(get_map_highscores(map_id=map_id, **search_params), default=lambda o: str(o)), status=200, mimetype="application/json")
    return resp

def search(filters=None, ordering=None, limit=None, all_skins=False, all_scores=False, per_skin=True, start_date=None, end_date=None):
    if not limit:
        limit = 1000
    if filters is None:
        filters = []

    # get the highscores NOT ORDERED
    query = db.session.query(
        Highscore.username,
        Map.name.label("mapname"),
        Map.id.label("map_id"),
        Highscore.skin,
        Highscore.time,
        Highscore.time_string,
        Highscore.datetime)

    if not all_scores:
        combination_column_names = [
            "username",
            "map_id"
        ]
        if per_skin:
            combination_column_names.append("skin")
        combination_columns = [getattr(Highscore, c) for c in combination_column_names]
        # subquery to get the best time for each combination e.g. (User, Skin, Map)
        best_scores = db.session.query(db.func.min(Highscore.time).label("time"),
                                       *combination_columns) \
                                .group_by(*combination_columns).subquery()
        join_filters = [ getattr(Highscore, c) == getattr(best_scores.c, c) for c in combination_column_names]
        query = query.select_from(
            Map,
            db.join(Highscore,
                    best_scores,
                    and_(
                        Highscore.time == best_scores.c.time,
                        *join_filters)))

    if not all_skins:
        query = query.filter(Highscore.skin.in_(base_skins))

    query = query.filter(Map.id == Highscore.map_id)

    if ordering is not None:
        query = query.order_by(ordering)

    for filter in filters:
        query = query.filter(filter)

    if start_date is not None:
        query = query.filter(Highscore.datetime >= start_date)

    if end_date is not None:
        query = query.filter(Highscore.datetime <= end_date)

    query = query.order_by(Highscore.time.asc())

    query = query.limit(limit)

    return query.all()

def parse_search_params():
    params = {}

    all_scores = request.args.get("all_scores") == "on"
    all_skins = request.args.get("all_skins") == "on"
    per_skin = request.args.get("per_skin") != "off"
    no_fuzzy = request.args.get('fuzzy') == "off"
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # request the params for the ordering
    order = request.args.get('order')
    descending = 'descending' in request.args

    ordering = None
    # if the order param is valid
    if order in key_to_column:
        # order by the order parameter
        order_by = key_to_column[order]
        # if the descending parameter got passed
        if descending:
            # order in descending order
            order_by = order_by.desc()
        ordering = order_by

    filters=[]
    # for every given parameter
    for key in request.args:
        # if the parameter's key is in the highscores columns
        if key in key_to_column:
            value = request.args.get(key)
            column = key_to_column[key]
            try:
                values = json.loads(value)
                assert isinstance(values, list)
                if not no_fuzzy:
                    values = [get_fuzzy(key, value) for value in values]
                filters.append(column.in_(values))
            except (JSONDecodeError, AssertionError):
                if not no_fuzzy:
                    value = get_fuzzy(key, value)
                filters.append(column == value)

    limit = request.args.get('limit',None)
    if limit:
        try:
            params['limit'] = int(limit)
        except (ValueError, TypeError):
            return jsonify(error="Invalid limit"), 400

    params['all_scores']  = all_scores
    params['all_skins']   = all_skins
    params['per_skin']    = per_skin
    params['ordering']    = ordering
    params['filters']     = filters
    if start_date:
        params['start_date']  = start_date
    if end_date:
        params['end_date']    = end_date
    return params

# when the route is api/search
@api_routes.route('/search')
def api_search():
    params = parse_search_params()
    scores = search(**params)
    # return the query as json
    resp = Response(response=to_json(scores), status=200, mimetype="application/json")
    return resp

def get_server_info(ip=Config.srb2_server, port=5029):
    q = SRB2Query(ip, port)
    serverpkt, playerpkt = q.askinfo()
    serverinfo = {}
    serverinfo['servername'] = serverpkt.servername
    serverinfo['version'] = serverpkt.version
    serverinfo['number_of_players'] = serverpkt.numberofplayer
    serverinfo['max_players'] = serverpkt.maxplayer
    serverinfo['leveltime'] = serverpkt.leveltime
    serverinfo['leveltime_string'] = tics_to_string(serverpkt.leveltime)
    serverinfo['filesneeded'] = serverpkt.filesneeded
    serverinfo['map'] = {
        'id': serverpkt.map['num'],
        'name': serverpkt.map['title'],
    }
    # Retrieve more map info if it is a known map
    servermap = get_maps(serverpkt.map['num']-1)
    if servermap:
        serverinfo['map'] = servermap.get_dict()
    serverinfo['players'] = []
    for player in playerpkt.players:
        player.pop("address")
        serverinfo['players'].append(player)
    return serverinfo

@api_routes.route('/server_info')
@api_routes.route('/server_info/<ip_address>')
@api_routes.route('/server_info/<ip_address>/<port>')
def server_info(ip_address=Config.srb2_server, port=5029):
    response = json.dumps(
        get_server_info(ip_address, port),
        default=lambda x: str(x))
    resp = Response(response=response, status=200, mimetype="application/json")
    return resp

@api_routes.route('/num_plays', defaults={'start_date': "2020-09-10"})
@api_routes.route('/num_plays/<start_date>')
def num_plays(start_date):
    return Response(response=to_json(get_num_plays(start_date)), status=200, mimetype="application/json")

@api_routes.route('/time_stats')
def time_stats():
    day = "day" in request.args
    hour = "hour" in request.args

    response = json.dumps(
        get_time_stats(day, hour),
        default=lambda x: str(x)
    )
    return Response(response=response, status=200, mimetype="application/json")

@api_routes.errorhandler(Exception)
def handle_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@api_routes.after_request
def set_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response
