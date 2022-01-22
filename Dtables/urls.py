from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.user_signup, name='Signup'),
    path('login/', views.user_login, name='Login'),
    path('createtable/', views.create_table, name='Create Table'),
    path('deletetable/', views.delete_table, name='Delete Table'),
]