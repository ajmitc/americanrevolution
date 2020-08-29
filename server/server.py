from markupsafe import escape

from flask import Flask, render_template, request, session, redirect, url_for, flash
app = Flask(__name__)


app.secret_key = b'.9#y7L"F4L8t\n\xec]/'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', name=escape(session['username']))
    return redirect(url_for("login"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        app.logger.info("Logging in user '{}'".format(request.args.get('username', '...')))
        if valid_login(request.args.get('username', None), request.args.get('password', None)):
            session['username'] = request.args.get("username", "")
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
    return True
