from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='Register User'),
    path('auth/login-password/', views.login_with_password, name='Login With Password'),
    path('auth/login-phone/', views.login_with_phone, name='Login With Phone'),

    path('note/', views.create_note, name='Create Note'),
    path('note/mark_suicidal/', views.mark_note_as_suicidal, name='Mark Note As Suicidal'),
    path('notes/', views.user_notes, name='Retrieve Notes'),

    path('mood/', views.register_mood, name='Register Mood'),
]