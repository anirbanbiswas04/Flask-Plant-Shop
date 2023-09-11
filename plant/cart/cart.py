from plant.shop.models import Product

class Cart(object):
    def __init__(self, session):
        self.session = session
        self.cart = session.get('cart', None)

        if not self.cart:
            cart = session['cart'] = {}
            self.cart = cart

    def __iter__(self):
        for pk in self.cart.keys():
            self.cart[str(pk)]['product'] = Product.query.filter_by(id=int(pk)).first()

        for item in self.cart.values():
            item['slug'] = item['product'].slug
            item['total_price'] = item['quantity'] * item['product'].price

            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, pk):
        if pk in self.cart:
            del self.cart[pk]
        self.save()

    def clear(self):
        self.cart = {}
        self.save()

    def add_or_update(self, pk, quantity=1):

        if not pk in self.cart:
            self.cart[pk] = {'quantity': quantity, 'product_id': pk}

        else:
            self.cart[pk]['quantity'] += int(quantity)
            
            if self.cart[pk]['quantity'] == 0:
                self.remove(pk)

        self.save()

    def get_item(self, pk):
        if str(pk) in self.cart:
            return self.cart[str(pk)]
        return None
    
    def get_total_amount(self):
        for pk in self.cart.keys():
            self.cart[str(pk)]['product'] = Product.query.filter_by(id=pk).first()
            
        return sum(item['quantity']*item['product'].price for item in self.cart.values())