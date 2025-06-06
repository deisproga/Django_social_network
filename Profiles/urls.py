from django.urls import path
from .views import users_page, UserListView, UserDetailView, WhoViewedMeView

urlpatterns = [
    path('users-page/', users_page, name='users_page'),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('who-viewed-me/', WhoViewedMeView.as_view()),
]