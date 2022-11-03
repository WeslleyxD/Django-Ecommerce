from .import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('active/<uidb64>/<token>', views.register_email_confirm, name='register_email_confirm'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('verification_email', views.verification_email, name='verification_email'),
]