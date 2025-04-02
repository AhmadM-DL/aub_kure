from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register_user, name='Register User'),
    path('auth/login-password/', views.login_with_password, name='Login With Password'),
    path('auth/login-phone/', views.login_with_phone, name='Login With Phone'),

    path('note/', views.create_note, name='create_note'),
    path('notes/', views.user_notes, name='retrieve_notes'),
]