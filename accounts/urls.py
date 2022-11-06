from .import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('active/<uidb64>/<token>', views.register_email_confirm, name='register_email_confirm'),
    path('login/', views.login_user, name='login_user'),
    path('login/2fa/', views.login_twofa_authentication, name='login_twofa_authentication'),
    path('login/2fa/<str:resend_mail>', views.login_twofa_authentication, name='resend_login_twofa_authentication'),
    path('logout/', views.logout_user, name='logout_user'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('verification_email', views.verification_email, name='verification_email'),
]