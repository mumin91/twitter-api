from django.contrib.auth import get_user_model
from django.db import models


class Follow(models.Model):
    source_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followed_by")
    destination_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followed")
    created = models.DateTimeField(auto_now_add=True)
