from .cart import Cart

def cart(request):
    cart = Cart(request)

    #print (dir(cart))
    # print (request.session.items())
    return {'cart': cart}