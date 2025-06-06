import json
from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import PostForm, CommentForm
from .models import Post, PostLike, Comment, CommentLike, Video, Message, Chat, Wish, Complaint, FriendRequest, \
    CustomUser, Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions
from .utils import send_notification_to_user


User = get_user_model()





@login_required
@require_POST
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    data = json.loads(request.body)
    text = data.get('text', '').strip()
    if not text:
        return JsonResponse({'error': 'Empty message'}, status=400)

    message = Message.objects.create(chat=chat, sender=request.user, text=text)
    return JsonResponse({
        'sender': message.sender.username,
        'text': message.text,
        'timestamp': message.timestamp.isoformat(),
    })


@login_required
def user_chats(request):
    chats = Chat.objects.filter(participants=request.user)
    data = []
    for chat in chats:
        participants = chat.participants.exclude(id=request.user.id).values_list('username', flat=True)
        data.append({
            "chat_id": chat.id,
            "participants": list(participants),
        })
    return JsonResponse(data, safe=False)

@login_required
def chat_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('timestamp')
    data = []
    for msg in messages:
        data.append({
            "sender": msg.sender.username,
            "text": msg.text,
            "timestamp": msg.timestamp.isoformat(),
        })
    return JsonResponse(data, safe=False)


@login_required
def chat_page(request):
    return render(request, 'myapp/chat.html')


def search_ajax(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        videos = Video.objects.filter(title__icontains=query)[:10]
        results = [{'id': v.id, 'title': v.title, 'url': v.url} for v in videos]
    return JsonResponse({'results': results})


def user_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj).order_by('-created_at')

    sent_request = None
    received_request = None

    if request.user.is_authenticated and request.user != user_obj:
        sent_request = FriendRequest.objects.filter(from_user=request.user, to_user=user_obj).first()
        received_request = FriendRequest.objects.filter(from_user=user_obj, to_user=request.user, accepted=False).first()

    context = {
        'profile_user': user_obj,
        'posts': posts,
        'sent_request': sent_request,
        'received_request': received_request,
    }

    return render(request, 'myapp/profile.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return Response({'status': 'ok'})


def my_profile_redirect(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    else:
        return redirect('login')


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    send_notification_to_user(post.author.id, f"{request.user.username} лайкнул твой пост")
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_list')

@login_required
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('post_list')


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = request.POST.get('post_id')
            comment.save()
            return redirect('post_list')

    return render(request, 'myapp/post_list.html', {
        'posts': posts,
        'comment_form': comment_form
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'myapp/create_post.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def about(request):
    return render(request, 'myapp/about.html')

def second(request):
    target_date = datetime(datetime.now().year, 8, 31, 23, 59, 59)
    return render(request, 'myapp/second.html', {'target_date': target_date.isoformat()})


@login_required
def notifications_view(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'myapp/notifications.html', {'notifications': notifications})


def home_view(request):
    User = get_user_model()
    user_count = User.objects.count()
    unread_notifications_count = 3


    context = {
        'user_count': user_count,
        'is_homepage': True,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'myapp/home.html', context)

@login_required
def profile_view(request):
    return render(request, 'myapp/profile.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def wish_board(request):
    wishes = Wish.objects.order_by('-likes', '-created_at')
    return render(request, 'myapp/wish_board.html', {'wishes': wishes})


@require_POST
def add_wish(request):
    text = request.POST.get('text', '').strip()
    if 0 < len(text) <= 300:
        Wish.objects.create(text=text)
    return redirect('wish_board')


@require_POST
def like_wish(request, wish_id):
    wishes_liked = request.session.get('wishes_liked', [])
    if wish_id not in wishes_liked:
        try:
            wish = Wish.objects.get(id=wish_id)
            wish.likes += 1
            wish.save()
            wishes_liked.append(wish_id)
            request.session['wishes_liked'] = wishes_liked
        except Wish.DoesNotExist:
            pass
    return redirect('wish_board')


@require_POST
def complain_wish(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)
    reason = request.POST.get('reason', '').strip()
    Complaint.objects.create(wish=wish, reason=reason)
    return redirect('wish_board')


def moderator_panel(request):
    complaints = Complaint.objects.select_related('wish').all().order_by('-created_at')
    return render(request, 'myapp/moderator_panel.html', {'complaints': complaints})


@require_POST
def delete_wish(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)
    wish.delete()
    return redirect('moderator_panel')


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if to_user == request.user:
        return redirect('profile', user_id=user_id)

    fr, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=to_user
    )

    if created:
        Notification.objects.create(
            user=to_user,
            message=f"{request.user.username} отправил(а) тебе заявку в друзья."
        )

    user = User.objects.get(id=user_id)
    return redirect('profile', username=user.username)

@login_required
def accept_friend_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.accepted = True
    fr.save()
    return redirect('profile', username=request.user.username)


@login_required
def cancel_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.filter(from_user=request.user, to_user=to_user).delete()
    return redirect('profile', username=request.user.username)

def user_search(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    return render(request, 'myapp/user_search.html', {'users': users, 'query': query})