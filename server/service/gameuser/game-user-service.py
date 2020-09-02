from markupsafe import escape

from flask import Flask, request
from service.common.datastore.sqllite import SQLiteDataStore
import json
import os
from uuid import uuid4
from service.common.consul_util import apply_consul_config
from service.common.prop_util import load_properties

app = Flask(__name__)

app.secret_key = os.urandom(16)

config = load_properties("service/gameuser/game-user-service.properties")
consul = apply_consul_config(app, config.get("Service", "name"), config.getint("Service", "port"), ['game-user', 'game-user-service'])


@app.route('/gameusers', methods=['GET'])
def get_game_user_endpoint():
    return get_game_users(request.args.get("id", None))


def get_game_users(id=None):
    with SQLiteDataStore() as db:
        sql = "SELECT * FROM game_user"
        where = []
        values = []
        if id is not None:
            where.append("id=?")
            values.append(id)
        if len(where) > 0:
            sql += " WHERE " + " AND ".join(where)
        rows = db.query(sql, values)
        return json.loads(rows)


@app.route('/gameuser', methods=['POST'])
def upsert_game_user_endpoint():
    success, message = upsert_game_user(json.loads(request.data))
    return message


def upsert_game_user(userdict):
    with SQLiteDataStore() as db:
        if 'id' in userdict.keys():
            sql = "UPDATE game_user SET "
            columns = []
            values = []
            for arg in userdict.keys():
                if arg in ["gameid", "userid", "allegiance", "rank", "location_id", "travel_status", "commander_user_id", "role"]:
                    columns.append("{}=?".format(arg))
                    values.append(userdict[arg])
            if len(columns) == 0:
                return True, "Nothing into update!"
            sql += ", ".join(columns)
            sql += " WHERE id=?"
            values.append(userdict['id'])
            db.execute(sql, values)
            return True, "Game user updated"
        else:
            userid = str(uuid4())
            sql = "INSERT INTO game_user(id, gameid, userid, allegiance, rank, location_id, travel_status, commander_user_id, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = [
                userid,
                escape(userdict['gameid']),
                escape(userdict['userid']),
                escape(userdict['allegiance']),
                escape(userdict['rank']),
                escape(userdict['location_id']),
                escape(userdict['travel_status']),
                escape(userdict['commander_user_id']),
                escape(userdict['role'])
            ]
            db.execute(sql, values)
            return True, "Game user created"
