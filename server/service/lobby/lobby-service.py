from markupsafe import escape
from service.common.consul_util import apply_consul_config, resolve_service
from service.common.prop_util import load_properties
from service.user.user_client import UserClient
from uuid import uuid4
import requests

from flask import Flask, render_template, request, session, redirect, url_for, flash
app = Flask(__name__, template_folder='../../templates')


app.secret_key = b'.9#y7L"F4L8t\n\xec]/'

config = load_properties("service/lobby/lobby.properties")
consul = apply_consul_config(app, config.get("Service", "name"), config.getint("Service", "port"), config.getlist('Service', 'tags'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', name=escape(session['username']))
    return redirect(url_for("login"))


@app.route('/register', methods=['POST'])
def register():
    error = None
    app.logger.info("Registering user '{}'".format(request.form.get('username', '...')))
    if user_exists(request.args.get('username', None)):
        flash('User already exists')
        return redirect(url_for("login"))
    else:
        userdict = {
            'name': request.form.get("name", ""),
            'username': request.form.get("username", ""),
            "password": request.form.get("password", "")
        }
        userclient = UserClient()
        userclient.update_user(userdict)
    return render_template('login.html', error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        app.logger.info("Logging in user '{}'".format(request.form.get('username', '...')))
        if valid_login(request.form.get('username', None), request.form.get('password', None)):
            session['username'] = request.form.get("username", "")
            flash('You were successfully logged in')
            return redirect(url_for("index"))
        else:
            flash('Invalid username/password', 'error')
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


def valid_login(username, password):
    userclient = UserClient()
    resp = userclient.login(username, password)
    if resp['success']:
        return True
    print(resp['message'])
    return False


def user_exists(username):
    userclient = UserClient()
    resp = userclient.get_user(username, {"username": username})
    if resp['success']:
        return True
    print(resp['message'])
    return False
