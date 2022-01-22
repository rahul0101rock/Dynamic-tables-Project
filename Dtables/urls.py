from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createtable/', views.create_table, name='Create Table'),
    path('deletetable/', views.delete_table, name='Delete Table'),
    path('logout/', views.user_logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]