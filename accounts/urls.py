from django.urls import path
from .views import user_login, user_logout, check_user_role, create_user, delete_user, get_users, get_csrf 

urlpatterns = [
    path('check_role/', check_user_role, name='check_role'),
    path('create_user/', create_user, name='create_user'),
    path('delete_user/', delete_user, name='delete_user'),
    path('get_users/', get_users, name='get_users'),
    path('get_csrf/', get_csrf, name='get_csrf'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]