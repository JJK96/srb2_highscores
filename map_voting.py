from flask import Flask, g, render_template, request, Blueprint
app = Flask(__name__)
import pymysql
from config import Config
from settings import host, username, password, voting_database

map_voting = Blueprint('map_voting', __name__)

mydb = pymysql.connect(
    host = host,
    user = username,
    passwd = password,
    database = voting_database,
    cursorclass = pymysql.cursors.DictCursor
)

c = mydb.cursor()

@map_voting.route('/')
def list():
    c.execute("select * from maps order by votes desc")
    maps = c.fetchall()
    return render_template('map_voting.html', maps=maps, config=Config)

@map_voting.route('/vote', methods = ['POST'])
def vote():
    map = int(request.form['map'])
    up = request.form['up'] == 'true'
    ip = request.remote_addr
    rowcount = c.execute("select * from voted where ip = '%s' and map = %d" % (ip, map))
    if rowcount > 0:
        return "You have already voted on this map", 403
    c.execute("update maps set votes = votes %s where id = %d;"
        % ('+1' if up else '-1', map))
    c.execute("insert into voted (ip, map) values ('%s', %d);" % (ip, map))
    mydb.commit()
    return "thanks"
