from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    #url авторизации по умолчанию
    path('', include('django.contrib.auth.urls')),
    #страница для регистрации
    path('register/', views.register, name='register'),
]