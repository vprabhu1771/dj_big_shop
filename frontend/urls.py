from django.urls import path

from frontend.views import forget_password, home, login

urlpatterns = [
    path('', home),
    # path('/', home, name='home'),
    path('login', login, name='login'),
    path('forget_password', forget_password),
]