from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.sellers_model import Seller
from flask_app.models.cars_model import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():

    if not Seller.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Seller.save(data)
    session['seller_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    seller = Seller.get_by_email(request.form)

    if not seller:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(seller.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['seller_id'] = seller.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'seller_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['seller_id']
    }
    return render_template("dashboard.html", seller=Seller.get_by_id(data), cars=Car.get_all_with_sellers())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')