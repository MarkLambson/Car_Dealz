from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.cars_model import Car
from flask_app.models.sellers_model import Seller


@app.route('/new/car')
def new_car():
    if 'seller_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['seller_id']
    }
    return render_template('new_car.html', seller=Seller.get_by_id(data))


@app.route('/create/car', methods=['POST'])
def create_car():
    if 'seller_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/new/car')
    data = {
        "price": request.form['price'],
        "model": request.form['model'],
        "make": request.form['make'],
        "year": request.form['year'],
        "description": request.form['description'],
        "seller_id": session['seller_id']
    }
    Car.save(data)
    return redirect('/dashboard')

@app.route('/edit/car/<int:id>')
def edit_car(id):
    if 'seller_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    seller_data = {
        "id":session['seller_id']
    }
    return render_template("edit_car.html", edit=Car.get_one(data), seller=Seller.get_by_id(seller_data))

@app.route('/update/car', methods=['POST'])
def update_car():
    if 'seller_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect(f'/edit/car/{request.form["id"]}')
    Car.update(request.form)
    return redirect('/dashboard')

@app.route('/car/<int:id>')
def show_car(id):
    if 'seller_id' not in session:
        return redirect('/logout')
    user_data = {
    "id":session['seller_id']
    }
    return render_template("show_car.html", car=Car.get_one_with_seller(id), seller=Seller.get_by_id(user_data))

@app.route('/destroy/car/<int:id>')
def destroy_car(id):
    if 'seller_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Car.destroy(data)
    return redirect('/dashboard')