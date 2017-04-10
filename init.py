from flask import Flask, request, render_template
from flask import url_for, redirect, session, Response
from flask_wtf import Form
from wtforms import StringField, validators
from enum import IntEnum
from functools import wraps

import errors as err
import db

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

app.jinja_env.line_statement_prefix = '#'  # enables jinja2 line mode
app.jinja_env.line_comment_prefix = '##'  # enables jinja2 line mode
app.secret_key = 'Bd\xf2\x14\xbbi\x01Gq\xc6\x87\x10BVc\x9c\xa4\x08\xdbk%\xfa*\xe3'  # os.urandom(24)

class Role(IntEnum):
    ADMIN = 1
    PROFESSOR = 2
    STUDENT = 3
    PARENT = 4

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not 'role' in session:
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
            if session['role'] not in roles:
                raise err.Forbidden('You do not have permission to access this page'
                                    )  # proper would be 401 Unauthorized
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def adminonly(fn):
    """ Decorator
    Checks if the user is currently an admin
    If not, redirect to admin-login
    """
    @wraps(fn)
    def go(*args, **kwargs):
        if 'role' in session and session['role'] == 'Admin':
        #if 'mod' in session:
            return fn(*args, **kwargs)
        else:
            raise err.Forbidden('You must be an admin to see this page'
                                )  # proper would be 401 Unauthorized
    return go

class LoginForm(Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = StringField('password', validators=[validators.DataRequired()])


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/index')
@requires_roles(Role.STUDENT, Role.PROFESSOR, Role.ADMIN, Role.PARENT)
def index():
    return render_template('index.html', session=session)

@app.route('/security')
def sec():
    data = db.getAllSecurity()
    return render_template('secview.html', data=data)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear() # wipes out the cookie
    return redirect('/index')
    #return render_template('logout.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        data = db.login(form.username.data, form.password.data)
        if not data:
            raise err.BadInput('Incorrect Username/Password')
        session['username'] = data['username']
        session['role'] = int(data['SecurityLevel'])
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.errorhandler(err.BadInput)
def handle_badinput(error):
    return render_template('error.html', error_message=error.message), 415


@app.errorhandler(err.e404)
def handle_e404(error):
    return render_template('error.html', error_message=error.message), 404


@app.errorhandler(err.BadMedia)
def handle_badmedia(error):
    return render_template('error.html', error_message=error.message), 415


@app.errorhandler(err.PermDenied)
def handle_permdenied(error):
    return render_template('error.html', error_message=error.message), 550


@app.errorhandler(err.Forbidden)
def handle_Forbidden(error):
    return render_template('error.html', error_message=error.message), 403


@app.errorhandler(err.DNE)
def handle_DNE(error):
    return render_template('error.html', error_message=error.message), 404
