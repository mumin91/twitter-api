import typing

from django.db import models
from django.db.models import QuerySet

from applibs.logger import general_logger
from twitter.models import CustomUser


class TweetManager(models.Manager):
    def get_by_author(self, author_id: int) -> typing.Optional[QuerySet["Tweet"]]:
        try:
            return (
                self.values("id", "text", "created", "modified")
                .filter(author_id=author_id)
                .order_by("-modified")
            )
        except Exception as e:
            general_logger.exception(e)
            return None

    def get_by_authors(
        self, author_ids: typing.List[int]
    ) -> typing.Optional[QuerySet["Tweet"]]:
        try:
            return (
                self.values("id", "author_id", "text", "created", "modified")
                .filter(author_id__in=author_ids)
                .order_by("-modified")
            )
        except Exception as e:
            general_logger.exception(e)
            return None


class Tweet(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = TweetManager()
