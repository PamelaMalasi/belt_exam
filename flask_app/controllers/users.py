from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_register(request.form):
        return redirect('/')
  
    email_data = {
        "email": request.form['email']
    }
    if User.find_email(email_data):
        flash("This account already exists. Please log in.")
        return redirect('/')
    
    pwhash = bcrypt.generate_password_hash(request.form['password'])
    print(pwhash)
    
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwhash
    }
    user_info = User.add_user(data)
   
    session['user_id'] = user_info
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    email_data = {
        "email": request.form['email-login']
    }
    user_in_db = User.find_email(email_data)
    if not user_in_db:
        flash("This account doesn't exist. Please try again.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password-login']):
        flash("Password is incorrect. Please try again.")
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        data = {
            "id": session['user_id']
        }
    user = User.find_id(data)
    all_cars = Car.all_cars()
    seller_info = Car.seller()
    purchases = Car.view_purchases(data)
    return render_template('dashboard.html', purchases=purchases,user=user, all_cars=all_cars,seller_info=seller_info)

@app.route('/end')
def end_session():
    session.clear()
    return redirect('/')

