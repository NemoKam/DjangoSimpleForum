from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/', authapp.user_register, name='register'),
    path('login/', authapp.user_login, name='login'),
    path('logout/', authapp.user_logout, name='logout'),
    path('verify_email/<str:activation_key>', authapp.user_verify_email, name='verify_email'),
]