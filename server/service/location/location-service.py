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

config = load_properties("service/location/location-service.properties")
consul = apply_consul_config(app, config.get("Service", "name"), config.getint("Service", "port"), config.getlist("Service", "tags"))


@app.route('/locations', methods=['GET'])
def get_locations_endpoint():
    return get_locations(request.args.get("id", None))


def get_locations(id=None):
    with SQLiteDataStore() as db:
        sql = "SELECT * FROM location"
        where = []
        values = []
        if id is not None:
            where.append("id=?")
            values.append(id)
        if len(where) > 0:
            sql += " WHERE " + " AND ".join(where)
        rows = db.query(sql, values)
        return json.loads(rows)


@app.route('/location', methods=['POST'])
def upsert_location_endpoint():
    success, message = upsert_location(json.loads(request.data))
    return message


def upsert_location(locdict):
    with SQLiteDataStore() as db:
        if 'id' in locdict.keys():
            sql = "UPDATE location SET "
            columns = []
            values = []
            for arg in locdict.keys():
                if arg in ["name", "x", "y"]:
                    columns.append("{}=?".format(arg))
                    values.append(locdict[arg])
            if len(columns) == 0:
                return True, "Nothing into update!"
            sql += ", ".join(columns)
            sql += " WHERE id=?"
            values.append(locdict['id'])
            db.execute(sql, values)
            return True, "Location updated"
        else:
            locid = str(uuid4())
            sql = "INSERT INTO location(id, name, x, y) VALUES (?, ?, ?, ?)"
            values = [
                locid,
                escape(locdict['name']),
                escape(locdict['x']),
                escape(locdict['y']),
            ]
            db.execute(sql, values)
            return True, "Location created"
