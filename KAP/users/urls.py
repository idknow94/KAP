from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', CampionSignupView.as_view(), name='signup'),
    path('edit/', edit_profile, name='edit_profile'),
    path('verify/<uidb64>/<token>/',
         VerifyEmailView.as_view(), name='verify_email'),
    path('<str:username>/', profile_view, name='profile'),
]
