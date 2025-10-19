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
    path('issue/<int:issue_id>/delete', views.issue_delete, name='issue_delete'),
    path('issue/<int:issue_id>/change_status',
         views.change_issue_status, name='change_issue_status'),
    path('comment/<int:comment_id>/delete',
         views.comment_delete, name='comment_delete'),
    path('comment/<int:comment_id>/like/', views.comment_like_toggle,
         name='comment_like_toggle'),  # Like/Unlike
    path('comment/<int:issue_id>/add/', views.add_comment,
         name='add_comment'),  # Add comment
]
