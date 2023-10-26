from flask import Blueprint, render_template, request, flash, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from middleware import authentication, guest

auth_page = Blueprint('auth', __name__, static_folder='static', template_folder='templates')
db = SQLAlchemy()

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