import typing

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet

from applibs.logger import general_logger


class FollowManager(models.Manager):
    def get_followed_ids(
        self, source_user_id: int
    ) -> typing.Optional[QuerySet["Follow"]]:
        try:
            return self.values_list("destination_user_id", flat=True).filter(
                source_user_id=source_user_id
            )
        except Exception as e:
            general_logger.exception(e)
            return None


class Follow(models.Model):
    source_user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="followed_by"
    )
    destination_user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="followed"
    )
    created = models.DateTimeField(auto_now_add=True)

    objects = FollowManager()
