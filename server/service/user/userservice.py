from markupsafe import escape

from flask import Flask, request
from datastore.sqllite import SQLiteDataStore
import json
import time
import os
from datetime import datetime, timedelta
from uuid import uuid4
from common.consul_util import apply_consul_config
from common.prop_util import load_properties

app = Flask(__name__)

app.secret_key = os.urandom(16)

config = load_properties("userservice.properties")

apply_consul_config(app, config.get("Service", "name"), config.get("Service", "port"), ['user', 'userservice'])


@app.route('/user', methods=['GET'])
def get_user_endpoint():
    return get_user(request.args.get("id", None))


def get_user(id=None):
    with SQLiteDataStore() as db:
        sql = "SELECT id, username, last_login, created_at FROM user_account"
        where = []
        values = []
        if id is not None:
            where.append("id=?")
            values.append(id)
        if len(where) > 0:
            sql += " WHERE " + " AND ".join(where)
        rows = db.query(sql, values)
        return json.loads(rows)


@app.route('/user', methods=['POST'])
def upsert_user_endpoint():
    success, message = upsert_user(json.loads(request.data))
    return message


@app.route('/login', methods=['POST'])
def login():
    with SQLiteDataStore() as db:
        userinfo = json.loads(request.data)
        sql = "SELECT * FROM user_account WHERE username=? AND password=?"
        values = [userinfo['username'], userinfo['password']]
        rows = db.query(sql, values)
        if len(rows) == 1:
            access_token = str(uuid4())
            expiration = datetime.utcnow()
            expiration = expiration + timedelta(hours=24)
            upsert_user({
                "id": rows[0]['id'],
                "last_login": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                "access_token": access_token,
                "access_token_expiration": expiration.strftime("%Y-%m-%d %H:%M:%S")
            })
            return {"success": True, "message": "User logged in"}
        return {"success": False, "message": "Unable to find user account"}


@app.route('/validate', methods=['POST'])
def validate():
    with SQLiteDataStore() as db:
        userinfo = json.loads(request.data)
        sql = "SELECT * FROM user_account WHERE username=? AND access_token=?"
        values = [userinfo['username'], userinfo['access_token']]
        rows = db.query(sql, values)
        if len(rows) == 1:
            # Check access_token_expiration
            expiration_text = rows[0]['access_token_expiration']
            expiration = datetime.strptime(expiration_text, "%Y-%m-%d %H:%M:%S")
            if expiration > datetime.utcnow():
                return {"success": True, "message": "User validated"}
            return {"success": False, "message": "Access Token expired"}
        return {"success": False, "message": "User not validated"}


def upsert_user(userdict):
    with SQLiteDataStore() as db:
        if 'id' in userdict.keys():
            sql = "UPDATE user_account SET "
            columns = []
            values = []
            for arg in userdict.keys():
                if arg in ["username", "password", "name", "last_login", "access_token", "access_token_expiration"]:
                    columns.append("{}=?".format(arg))
                    values.append(userdict[arg])
            if len(columns) == 0:
                return True, "Nothing into update!"
            sql += ", ".join(columns)
            sql += " WHERE id=?"
            values.append(userdict['id'])
            db.execute(sql, values)
            return True, "User account updated"
        else:
            userid = str(uuid4())
            sql = "INSERT INTO user_account(id, username, password, name, created_at) VALUES (?, ?, ?, ?, ?)"
            values = [
                userid,
                escape(userdict['username']),
                escape(userdict['password']),
                escape(userdict['name']),
                time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            ]
            db.execute(sql, values)
            return True, "User account created"
