from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, home_view, about, second, create_post, \
    post_list, like_comment, like_post, user_profile, my_profile_redirect, notifications_view, mark_notifications_read, \
    search_ajax, chat_messages, user_chats, chat_page, send_message, wish_board, add_wish, like_wish, moderator_panel, \
    delete_wish, complain_wish, cancel_friend_request, accept_friend_request, send_friend_request, user_search

urlpatterns = [
    path('users/', user_search, name='user_search'),
    path('send-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('cancel-request/<int:user_id>/', cancel_friend_request, name='cancel_friend_request'),
    path('complain/<int:wish_id>/', complain_wish, name='complain_wish'),
    path('moderator/', moderator_panel, name='moderator_panel'),
    path('moderator/delete/<int:wish_id>/', delete_wish, name='delete_wish'),
    path('about/wish/', wish_board, name='wish_board'),
    path('add/', add_wish, name='add_wish'),
    path('like/<int:wish_id>/', like_wish, name='like_wish'),
    path('notifications/read/', mark_notifications_read),
    path('search/', search_ajax, name='search'),
    path('chat/', chat_page, name='chat_page'),
    path('api/user_chats/', user_chats, name='user_chats'),
    path('api/chat_messages/<int:chat_id>/', chat_messages, name='chat_messages'),
    path('api/send_message/<int:chat_id>/', send_message, name='send_message'),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('profile/<str:username>/', user_profile, name='profile'),
    path('comments/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('posts/new/', create_post, name='create_post'),
    path('notifications/', notifications_view, name='notifications'),
    path('second/', second, name='second'),
    path('about/', about, name='about'),
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', my_profile_redirect, name='my_profile'),
]
