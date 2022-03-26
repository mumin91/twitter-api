from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from applibs.fake import fake
from twitter.models import CustomUser, Follow


class FollowUnfollowViewTest(APITestCase):
    def setUp(self) -> None:
        self.follow_unfollow_url = reverse("follow_unfollow_user")

        self.profile_1 = fake.profile()
        self.profile_2 = fake.profile()

        self.user_1 = CustomUser.objects.create_user(
            username=self.profile_1.get("username"),
            password="demo_password",
            first_name=self.profile_1.get("name").split()[0],
            last_name=self.profile_1.get("name").split()[1],
            email=self.profile_1.get("mail"),
        )

        self.user_2 = CustomUser.objects.create_user(
            username=self.profile_2.get("username"),
            password="demo_password",
            first_name=self.profile_2.get("name").split()[0],
            last_name=self.profile_2.get("name").split()[1],
            email=self.profile_2.get("mail"),
        )

        self.user_1_token = Token.objects.create(user=self.user_1)
        self.user_2_token = Token.objects.create(user=self.user_2)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_1_token.key)

    def tearDown(self) -> None:
        CustomUser.objects.all().delete()
        Token.objects.all().delete()
        Follow.objects.all().delete()

    def test_follow_success_response(self):
        payload = {"target_user_id": self.user_2.id}

        response = self.client.post(self.follow_unfollow_url, payload, format="json")

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="response status ok"
        )
        self.assertEqual(response.data, "User followed", msg="response body ok")

    def test_follow_model_after_success_response(self):
        payload = {"target_user_id": self.user_2.id}
        _ = self.client.post(self.follow_unfollow_url, payload, format="json")

        follow_objs = Follow.objects.all()

        self.assertEqual(follow_objs.count(), 1, msg="single object created")

        follow_obj = follow_objs[0]

        self.assertEqual(follow_obj.destination_user_id, self.user_2.id)
        self.assertEqual(follow_obj.source_user_id, self.user_1.id)

    def test_follow_validation_error_response(self):
        payload = {"target_user_id": "slkafdjkfj"}
        error_response = {
            "target_user_id": [
                ErrorDetail(string="A valid integer is required.", code="invalid")
            ]
        }

        response = self.client.post(self.follow_unfollow_url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="failed response status ok",
        )
        self.assertEqual(response.data, error_response, msg="error response body ok")

    def test_follow_exception_error_response(self):
        payload = {"target_user_id": 11111}
        error_response = "Target user not found"

        response = self.client.post(self.follow_unfollow_url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="failed response status ok",
        )
        self.assertEqual(response.data, error_response, msg="error response body ok")
