from markupsafe import escape

from flask import Flask, request
from service.common.datastore.sqllite import SQLiteDataStore
import json
import time
import os
from uuid import uuid4
from service.common.consul_util import apply_consul_config
from service.common.prop_util import load_properties

app = Flask(__name__)

app.secret_key = os.urandom(16)

config = load_properties("service/game/game-service.properties")
consul = apply_consul_config(app, config.get("Service", "name"), config.getint("Service", "port"), config.getlist("Service", "tags"))


@app.route('/games', methods=['GET'])
def get_games_endpoint():
    return get_games(request.args.get("id", None))


def get_games(id=None):
    with SQLiteDataStore() as db:
        sql = "SELECT * FROM game"
        where = []
        values = []
        if id is not None:
            where.append("id=?")
            values.append(id)
        if len(where) > 0:
            sql += " WHERE " + " AND ".join(where)
        rows = db.query(sql, values)
        return json.loads(rows)


@app.route('/game', methods=['POST'])
def upsert_game_endpoint():
    success, message = upsert_game(json.loads(request.data))
    return message


def upsert_game(gamedict):
    with SQLiteDataStore() as db:
        if 'id' in gamedict.keys():
            sql = "UPDATE game SET "
            columns = []
            values = []
            for arg in gamedict.keys():
                if arg in ["name", "created_at"]:
                    columns.append("{}=?".format(arg))
                    values.append(gamedict[arg])
            if len(columns) == 0:
                return True, "Nothing into update!"
            sql += ", ".join(columns)
            sql += " WHERE id=?"
            values.append(gamedict['id'])
            db.execute(sql, values)
            return True, "Game updated"
        else:
            gameid = str(uuid4())
            sql = "INSERT INTO game(id, name, created_at) VALUES (?, ?, ?)"
            values = [
                gameid,
                escape(gamedict['name']),
                time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            ]
            db.execute(sql, values)
            return True, "Game created"
