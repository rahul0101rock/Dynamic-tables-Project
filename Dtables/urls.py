from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createtable/', views.create_table, name='Create Table'),
    path('deletetable/', views.delete_table, name='Delete Table'),
    path('insertdata/', views.insert_data, name='Insert Data'),
    path('deletedata/', views.delete_data, name='Delete Data'),
    path('table/<table_name>', views.view_table,name='View Table'),
    path('auditLogs',views.audit_logs, name='Audit Logs'),
    path('logout/', views.user_logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]