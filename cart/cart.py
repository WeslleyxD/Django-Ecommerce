from decimal import Decimal
from django.conf import settings
from products.models import Product
from coupon.models import Coupon

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, None)
        if not cart:
        # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id', None)

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] + quantity < 1:
                self.cart[product_id]['quantity'] += quantity
                self.save()
            else:
                self.remove(product)

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            # print ('CART')
            # print (self.cart)
            del self.cart[product_id]
            self.save()

    def remove_coupon(self):
        # print ('SESSION')
        # print (self.session.keys())
        # print ('coupon_id' in self.session.keys())

        if 'coupon_id' in self.session.keys():
            del self.session['coupon_id']
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        
    def get_quantity_products(self):
        return len(self.cart)

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
            return None
            

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()



