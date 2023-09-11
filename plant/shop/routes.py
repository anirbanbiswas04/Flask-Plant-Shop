from flask import Blueprint, render_template, request, session
from plant.shop.models import Product, Category
from plant.cart.cart import Cart
from plant import db

shop = Blueprint('shop', __name__)


@shop.route('/details/<slug>', methods=['POST', 'GET'])
def details(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    if request.method == 'POST':
        item = request.form.get('product_id', None)
        if item:
            cart = Cart(session)
            cart.add_or_update(item)
        return render_template('parts/cart_menu.html')
    return render_template('details.html', product=product)


@shop.route('/search')
def search():
    query = request.args.get('query', None)
    page = request.args.get('page', 1)
    per_page = 8
    products =  []

    if query:
        products = Product.query.filter(db.or_(
            Product.name.icontains(query),
            Product.description.icontains(query)
        )).paginate(
            page=int(page),
            per_page=per_page
            )

    return render_template('search.html', products=products, query=query)


@shop.route('/main-shop')
def main_shop():
    categories = Category.query.all()
    category_selected = request.args.get('category', None)
    page = request.args.get('page', 1)
    per_page = 8
    products = Product.query.paginate(page=int(page), per_page=per_page) if not category_selected else Product.query.filter_by(
        category_id=category_selected
        ).paginate(page=int(page), per_page=per_page)

    context = {
        'categories': categories,
        'products': products, 
        'category_selected': category_selected, 
        'category_name': Category.query.filter_by(id=category_selected).first().name if category_selected else None
    }
    return render_template('shop.html', **context)