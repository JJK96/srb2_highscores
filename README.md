# SRB2 Highscores

Frontend for the data extracted using https://github.com/JJK96/SRB2/tree/speedrun_server

And a page for voting on maps

## Setup

1. Install the dependencies in `requirements.txt`.
```
pip install -r requirements.txt
```
2. Populate a database with data in `sql/map_voting.sql`, this is the map_voting database
2. Create `settings.py` with the following contents:
```
username = "<database_username>"
password = "<database_password>"
host = "<database_hostname>"
highscores_database = "<highscores_database_name>"
voting_database = "<map_voting_database_name>"
```
3. `python app.py`

Alternatively [wsgi](wsgi.org) can be used to run it in combination with an HTTP server.

## Upgrade the database

If a change has been made to the database, the migrations should be run using
```
flask db upgrade
```
