from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from twitter.models import Tweet


class MyTweetsView(ListAPIView):

    def list(self, request: Request, *args, **kwargs) -> Response:
        if tweets := Tweet.objects.get_by_user(request.user.id):
            return Response(data=tweets, status=status.HTTP_200_OK)
        return Response("No tweet found", status=status.HTTP_204_NO_CONTENT)
