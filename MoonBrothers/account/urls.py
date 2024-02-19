from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.signin, name='signin'),
    path('logout', views.logout_request, name='logout'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("profile", views.profile, name='profile')
]