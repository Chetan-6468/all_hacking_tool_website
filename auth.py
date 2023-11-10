from flask import Blueprint, render_template, request, flash, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from middleware import authentication, guest
from google_auth_oauthlib.flow import Flow
# import os
# import pathlib 


auth_page = Blueprint('auth', __name__, static_folder='static', template_folder='templates')
db = SQLAlchemy()

# os.environ['OAUTH2LIB_INSECURE_TRANSPORT'] = '1'

# GOOGLE_CLIENT_ID = "760608333724-usp9lttq0h948n6s5ocbn716e8occmj3.apps.googleusercontent.com"

# client_secrets_file = os.path.join(pathlib.path(__file__).parent,"client_secrets.json")

# flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                    #  scopes =["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email", "openid"],
                                    #  redirect_uri="http://127.0.0.1:5000/auth/signup"
                                    #  )






class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

@auth_page.route('/signup', methods=['GET','POST'])
@guest
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']


        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email address already in use. Please choose another one.")
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Successfully")
            return redirect("/auth/signin")

    return render_template('signup.html')

@auth_page.route('/signin', methods=['GET','POST'])
@guest
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/home')
        
        else:
            return render_template('signin.html',error="Invalid user")


    return render_template('signin.html')


@auth_page.route('/profile')
def profile(): 
     user = User.query.filter_by(email=session['email']).first()
     return render_template('profile.html',user=user)  


@auth_page.route('/logout')
@authentication
def logout():
    session.pop('email',None)
    return redirect('/mainhome')