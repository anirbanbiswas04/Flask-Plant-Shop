from flask import Blueprint, render_template, request, redirect, flash, url_for
from plant.shop.models import Product
from flask_login import login_user, logout_user
from plant.core.models import User

core = Blueprint('core', __name__, static_folder='static')


@core.route('/')
def home():
    products = Product.query.all()[:8]
    return render_template('home.html', products=products)


@core.post('/admin-login')
def admin_login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password=password):
        login_user(user)
        return redirect('/admin')
    else:
        flash('Please check your username or password.', category='danger')
        return redirect('/admin')
        
@core.get('/admin-logout')
def admin_logout():
    logout_user()
    return redirect(url_for('core.home'))
     

