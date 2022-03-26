from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from applibs.pagination import TweetPagination
from twitter.models import Tweet, Follow
from twitter.serializers import TweetModelSerializer


class NewsfeedView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = TweetPagination
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        author_ids = Follow.objects.get_followed_ids(self.request.user.id)
        author_ids = list(author_ids)
        author_ids.append(self.request.user.id)

        return Tweet.objects.filter(author_id__in=self.request.user.id).order_by("-modified")
