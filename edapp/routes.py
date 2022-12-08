from distutils.log import error
from pickle import TRUE
from edapp import app
from flask import Flask, redirect, url_for
from flask import render_template, redirect, url_for, request, flash
import json
from edapp.utils import checkUserCredentials, createUser, get_random_string, getUserDataByEmail, responseHandler
from reg import users
from forms import loginform, registerform
from flask import request
from flask import Flask, session


def __repr__(self):
    return f'users{self.name,self.email,self.password}'


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):

    # defining function
    return render_template("noroute.html")


@app.route('/reg_redirect')
def reg_redirect():
    try:
        if("email" in session):
            user = getUserDataByEmail(session.get("email"))
            if (user is None):
                return redirect(url_for('login_redirect', error=""))
            return render_template("profile/profile.html", email=user.email, name=user.name)
        return render_template("auth/register.html",
                           form=registerform(), error=request.args['error'])
    except Exception as e:
        return render_template("auth/register.html",
                           form=registerform(), error="")

@app.route('/login_redirect')
def login_redirect():

    try:
        if("email" in session):
            user = getUserDataByEmail(session.get("email"))
            if (user is None):
                return redirect(url_for('login_redirect', error=""))
            return render_template("profile/profile.html", email=user.email, name=user.name)
        return render_template("auth/login.html",
                           form=loginform(), error=request.args['error'])

    except Exception as e:
        return render_template("auth/login.html",
                           form=loginform(), error="")



@app.route('/profile_redirect')
def profile_redirect():
    if("email" in session and request.args['email']==session.get("email")):
        user = getUserDataByEmail(session.get("email"))
        if (user is None):
            return redirect(url_for('login_redirect', error=""))
        return render_template("profile/profile.html", email=request.args['email'], name=request.args['name'])
    else:
        return redirect(url_for('login_redirect', error=""))


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/loggingOut')
def loggingOut():
    # session.clear()
    print("LOGINGGGGGGGGGGGGGGGGGGGGG")
    return render_template('home.html')


def moving():
    # Moving forward code
    print("Moving Forward...")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if (request.method == 'GET'):
        if ("email" in session):
            user = getUserDataByEmail(session.get("email"))
            if (user is None):
                return redirect(url_for('login_redirect', error="Email data not found"))
            return redirect(url_for('profile_redirect', email=session.get("email"), name=user.name))
        return redirect(url_for('reg_redirect', error=""))
    elif (request.args.get("resp") is None):
        if (request.form['name'] is None):
            return redirect(url_for('reg_redirect', error="name is required"))
        elif (request.form['email'] is None):
            return redirect(url_for('reg_redirect', error="email is required"))
        elif (request.form['password'] is None):
            return redirect(url_for('reg_redirect', error="password is required"))
        elif (request.form['repeat_password'] is None):
            return redirect(url_for('reg_redirect', error="repeat password is required"))
        elif (request.form['password'] != request.form['repeat_password']):
            return redirect(url_for('reg_redirect', error="password is not matched"))
        data = createUser(
            request.form['name'], request.form['email'], request.form['password'])
        if (data.get("status") == True):
            return redirect(url_for('login_redirect', error=""))
        else:
            return redirect(url_for('reg_redirect', error=data.get("message")))

    elif (request.args.get("resp") == "API"):
        dataa = json.loads(request.data)
        return createUser(dataa.get("name"), dataa.get("email"), dataa.get("password"))
    else:
        return responseHandler(False, {}, "required param resp with value API")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        if ("email" in session):
            user = getUserDataByEmail(session.get("email"))
            if (user is None):
                return redirect(url_for('login_redirect', error="Email data not found"))
            return redirect(url_for('profile_redirect', email=session.get("email"), name=user.name))
        return redirect(url_for('login_redirect', error=""))
    else:
        if ("email" in session):
            return responseHandler(False, {}, "session already existed , please logout")
        elif (request.args.get("resp") is None):
            if (request.form['email'] is None):
                return redirect(url_for('login_redirect', error="email field required"))
            elif (request.form['password'] is None):
                return redirect(url_for('login_redirect', error="password field required"))
            if (checkUserCredentials(request.form['email'], request.form['password']) == True):
                session['email'] = request.form['email']
                user = getUserDataByEmail(request.form['email'])
                if (user is None):
                    return redirect(url_for('login_redirect', error="Email data not found"))
                return redirect(url_for('profile_redirect', email=user.email, name=user.name))
            else:
                return redirect(url_for('login_redirect', error="No data found this email"))

        elif (request.args.get("resp") == "API"):
            dataa = json.loads(request.data)
            if (dataa.get("email") is None):
                return responseHandler(False, {}, "email field required")
            elif (dataa.get("password") is None):
                return responseHandler(False, {}, "password field required")

            if (checkUserCredentials(dataa.get("email"), dataa.get("password")) == True):
                session['email'] = dataa.get("email")
                return responseHandler(True, {}, "Successfully loged in")
            else:
                return responseHandler(False, {}, "User not found")


@app.route('/profile/<email>', methods=['GET', 'POST'])
def profile(email=None):

    if (request.args.get("resp") is None):
        if (email is None):
            return responseHandler(False, {}, "Email required as param")
        elif ("email" in session and email == session.get("email")):
            user = getUserDataByEmail(email)
            if (user is None):
                return redirect(url_for('login_redirect', error="Email data not found"))
            return redirect(url_for('profile_redirect', email=email, name=user.name))
        else:
            return redirect(url_for("login"))

    elif (request.args.get("resp") == "API"):
        if (email is None):
            return responseHandler(False, {}, "Email required as param")
        elif ("email" in session and email == session.get("email")):
            user = getUserDataByEmail(email)
            if (user is None):
                return responseHandler(False, {}, "Email data not found")
            return responseHandler(True, {"email": email, "name": user.name}, "Session is existed")
        return responseHandler(False, {}, "Session is not existed on this email, please first login")


@app.route('/admin')
def admin():
    return render_template('admin/admin.html')


@app.route('/referrals')
def referral():
    return render_template('referral/referrals.html')


@app.route('/whatsappconsent')
def consent():
    return render_template('referral/whatsappconsent.html')


@app.route('/getAllUsers', methods=['GET', 'POST'])
def get():
    if ("email" in session):
        return responseHandler(True, str(users.query.all()), "list of users")
    return responseHandler(False, {}, "Session is not existed , please first login")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    if (request.args.get("resp") is None):
        return redirect(url_for('login_redirect', error=""))
    return responseHandler(True, {}, "Session cleared")


@app.route('/getCurruntSessionUser', methods=['GET', 'POST'])
def getCurruntSessionUser():
    if ("email" in session):
        return responseHandler(True, {}, session.get("email"))
    return responseHandler(False, {}, "Session is not existed , please first login")
