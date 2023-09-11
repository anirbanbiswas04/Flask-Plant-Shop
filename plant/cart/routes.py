from flask import Blueprint, render_template, session, url_for, redirect, make_response, request, flash
from plant import db
from plant.cart.cart import Cart
from plant.shop.models import Product, Order, OrderItem


cart =  Blueprint('cart', __name__)


@cart.route('/cart', methods=['GET', 'POST'])
def cart_page():
    return render_template('cart.html')

@cart.route('/cart-update/<product_id>/<action>')
def cart_update(product_id, action):
    cart = Cart(session)

    if action == 'increment':
        cart.add_or_update(product_id, 1)
    elif action == 'decrement':
        cart.add_or_update(product_id, -1)

    product = Product.query.filter_by(id=int(product_id)).first()
    cart_item = cart.get_item(product_id)

    if cart_item:
        item = {
            'product_id': product.id,
            'product': {
                'name': product.name,
                'price': product.price,
            },
            'slug': product.slug,
            'total_price': product.price * int(cart_item['quantity']),
            'quantity': cart_item['quantity'],
        }
    
    else:
        item = None

    response = make_response(render_template('parts/cart_item.html', item=item))
    response.headers["HX-Trigger"] = "update-cart-menu"
    return response


@cart.route('/get-cart-count')
def get_cart_count():
    return render_template('parts/cart_menu.html')

@cart.route('/get-total-amount')
def get_total_amount():
    return render_template('parts/total_amount.html')

@cart.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = Cart(session)
    if cart.__len__() == 0:
        return redirect(url_for('cart.cart_page'))
    
    if request.method == 'POST':
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        city = request.form['city']
        postal_code = int(request.form['postal_code'])
        state = request.form['state']
        phone_no = int(request.form['phone_no'])
        nearest_landmark = request.form['nearest_landmark']

        try:
            order = Order(
                full_name=full_name,
                email_address=email_address,
                city=city,
                postal_code=postal_code,
                state=state,
                phone_no=phone_no,
                nearest_landmark=nearest_landmark,
                total_amount=int(cart.get_total_amount())
            )
            db.session.add(order)

            for item in cart:
                order_item = OrderItem(
                    product_id = item['product_id'],
                    quantity = item['quantity'],
                    order_id = order.id
                )
                db.session.add(order_item)

            db.session.commit()

            cart.clear()
            return redirect(url_for('cart.success'))
        
        except:
            flash('Oops something went wrong...', category='error')
            return redirect(url_for('cart.checkout'))

    return render_template('checkout.html')

@cart.route('/succss')
def success():
    return render_template('success.html')