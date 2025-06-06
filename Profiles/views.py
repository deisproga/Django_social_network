from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .models import ProfileView
from .serializers import UserListSerializer, UserDetailSerializer


User = get_user_model()


def users_page(request):
    return render(request, 'myapp/users_page.html')


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        viewed_user = self.get_object()
        if viewed_user != request.user:
            ProfileView.objects.get_or_create(viewer=request.user, viewed=viewed_user)
        return super().retrieve(request, *args, **kwargs)

class WhoViewedMeView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(viewed_profiles__viewed=self.request.user)
