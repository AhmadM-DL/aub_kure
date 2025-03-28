from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [

    path('register/', views.register_user, name='Register User'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('note/', views.create_note, name='create_note'),
    path('notes/', views.user_notes, name='retrieve_notes'),
]