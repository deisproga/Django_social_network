from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileView(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views_made")
    viewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views_received")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('viewer', 'viewed')

    def __str__(self):
        return f"{self.viewer} смотрел(а) на {self.viewed}"

