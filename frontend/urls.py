from django.urls import path

from frontend.views import forget_password, home, login, register, about, account

urlpatterns = [
    path('', home, name='home'),
    # path('/', home, name='home'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('forget_password', forget_password),
    path('account', account, name='account'),
    path('about', about, name='about'),
]