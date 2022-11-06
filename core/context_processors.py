def user_authenticated(request):
    print (dir(request))
    print(request.session.values())
    if request.user.is_authenticated:
        context = {'user_authenticated': request.user.first_name}
    else:
        context = {'user_authenticated': 'bem-vindo'}
    
    return context