from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applibs.logger import general_logger
from twitter.models import Follow
from twitter.serializers import FollowSerializer


class FollowUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj, created = Follow.objects.get_or_create(
                source_user=request.user,
                destination_user_id=serializer.validated_data.get("target_user_id"),
            )
        except Exception as e:
            general_logger.exception(e)
            return Response("Action failed", status=status.HTTP_400_BAD_REQUEST)

        if obj and not created:
            obj.delete()
            return Response("User unfollowed", status=status.HTTP_200_OK)

        if created:
            return Response("User followed", status=status.HTTP_200_OK)
