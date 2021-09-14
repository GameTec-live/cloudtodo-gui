import flask
import os
import sys
import time
from threading import Thread

app = flask.Flask(__name__)

username = []
password = []
version = "0.0.1"
user = ""
enabled = False
lists = []

def read_settings():
    global enabled
    f = open("settings" , "r")
    enabled = f.read()
    f.close()

read_settings()

def read_users():
    global username
    f = open("users" , "r")
    username = f.read()
    username = username.split("\n")
    username = username[:-1]
    f.close()

read_users()

def read_passwd():
    global password
    f = open("passwd" , "r")
    password = f.read()
    password = password.split("\n")
    password = password[:-1]
    f.close()

read_passwd()

def read_lists():
    global lists
    files = os.listdir()
    for x in files:
        if x.endswith(".todolist"):
            print(x)
        else:
            files.remove(x)
    if len(files) > 0:
        lists = ""
        for x in files:
            if x.endswith(".todolist"):
                    lists = lists + x + "\n"
        lists = lists

read_lists()

@app.route('/', methods=['GET', 'POST'])
def index():
    global user
    global enabled
    global lists
    read_settings()
    read_passwd()
    read_users()
    read_lists()
    if enabled == "True":
        logged_in = flask.request.cookies.get('logged_in')
        if logged_in == "True":
            if flask.request.method == 'POST':
                if flask.request.form.get('Disable') == "Disable":
                    f = open("settings" , "w")
                    f.write("False")
                    f.close()
                elif flask.request.form.get('Logout') == 'Logout':
                    print("Logout")
                    return flask.redirect(flask.url_for('logout'))
                elif flask.request.form.get('Create') == 'Create':
                    cname = ""
                    cname = flask.request.form.get('name')
                    if os.path.exists(cname + ".todolist"):
                        cname = ""
                    else:
                        todolist = open(cname + ".todolist", "w")
                        todolist.close()
                        cname = ""
                elif flask.request.form.get('Create-user') == 'Create-user':
                    cuser = flask.request.form.get('username')
                    cpass = flask.request.form.get('password')
                    if cuser in username or cuser == "" or cpass == "":
                        pass
                    else:
                        f = open("users" , "a")
                        f.write(cuser + "\n")
                        f.close()
                        f = open("passwd" , "a")
                        f.write(cpass + "\n")
                        f.close()
                elif flask.request.form.get('Delete-user') == 'Delete-user':
                    cuser = flask.request.form.get('username')
                    cpass = flask.request.form.get('password')
                    if cuser not in username or cuser == "" or cpass == "":
                        pass
                    else:
                        f = open("users", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("users", "w")
                        for line in lines:
                            if line.strip("\n") != cuser:
                                f.write(line)
                        f.close()
                        f = open("passwd", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("passwd", "w")
                        for line in lines:
                            if line.strip("\n") != cpass:
                                f.write(line)
                        f.close()
                else:
                    pass
            elif flask.request.method == 'GET':
                return flask.render_template('index.html', form=flask.request.form, user=user, enabled=enabled, logged_in=logged_in, ping="None", version=version, username=username, lists=lists)
            return flask.render_template('index.html', user=user, enabled=enabled, logged_in=logged_in, ping="None", version=version, username=username, lists=lists)
        else:
            return flask.redirect(flask.url_for('login'))
    else:
        return flask.render_template('coming-soon.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    error = None
    if flask.request.method == 'POST':
        user = flask.request.form.get('username')
        if user in username and flask.request.form.get('password') in password:
            resp = flask.make_response(flask.redirect(flask.url_for('index')))
            if flask.request.form.get('remember') == 'on':
                resp.set_cookie('logged_in', 'True')
            else:
                resp.set_cookie('logged_in', 'True', max_age=120)
            return resp
        else:
            error = 'Invalid credentials. Please try again.'
    return flask.render_template('login.html', error=error)

@app.route('/logout')
def logout():
    resp = flask.make_response(flask.redirect(flask.url_for('index')))
    resp.set_cookie('logged_in', "False" , expires=0)
    return resp

def run():
  app.run(host='0.0.0.0', port=80)

def web():
  Thread(target=run).start()
  