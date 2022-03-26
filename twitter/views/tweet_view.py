from rest_framework.generics import CreateAPIView

from twitter.models import Tweet
from twitter.serializers import TweetSerializer


class TweetView(CreateAPIView):
    # TODO: Add urls images etc.
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
