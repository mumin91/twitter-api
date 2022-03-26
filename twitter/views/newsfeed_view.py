from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from twitter.models import Tweet, Follow


class NewsfeedView(ListAPIView):
    def list(self, request: Request, *args, **kwargs) -> Response:

        author_ids = Follow.objects.get_followed_ids(request.user.id)
        author_ids = list(author_ids)
        author_ids.append(request.user.id)

        if tweets := Tweet.objects.get_by_authors(author_ids):
            return Response(data=tweets, status=status.HTTP_200_OK)
        return Response("No tweet found", status=status.HTTP_204_NO_CONTENT)
