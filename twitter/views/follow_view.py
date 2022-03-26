from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from twitter.models import Follow, CustomUser
from twitter.serializers import FollowSerializer


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            destination_user = CustomUser.objects.get(
                pk=serializer.validated_data.get("target_user_id")
            )
        except CustomUser.DoesNotExist:
            return Response("Target user not found", status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(
            source_user_id=request.user.id,
            destination_user_id=destination_user.id,
        )

        return Response("User followed", status=status.HTTP_200_OK)
