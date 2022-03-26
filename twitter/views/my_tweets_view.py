from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from applibs.pagination import TweetPagination
from twitter.models import Tweet
from twitter.serializers import TweetModelSerializer


class MyTweetsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetModelSerializer
    pagination_class = TweetPagination

    def get_queryset(self):
        return Tweet.objects.filter(author_id=self.request.user.id)
