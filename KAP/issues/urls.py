from django.urls import path
from . import views

urlpatterns = [
    path('', views.issue_list, name='home'),  # Home page showing all issues
    path('issue/<int:issue_id>/', views.issue_detail,
         name='issue_detail'),  # Issue detail with comments
    path('issue/create/', views.create_issue,
         name='issue_create'),  # Raise new issue
    path('issue/<int:issue_id>/like/', views.issue_like_toggle,
         name='issue_like_toggle'),  # Like/Unlike
    path('signup/', views.signup_view, name='signup'),  # Sign up
    path('comment/<int:issue_id>/add/', views.add_comment,
         name='add_comment'),  # Add comment
]
