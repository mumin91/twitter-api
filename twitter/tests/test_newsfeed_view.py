from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from applibs.fake import fake
from twitter.models import CustomUser, Tweet, Follow


class NewsfeedViewTest(APITestCase):
    def setUp(self) -> None:
        self.newsfeed_url = reverse("newsfeed")
        self.limit_20_offset_1 = "?limit=20&offset=1"

        self.profile_1 = fake.profile()
        self.profile_2 = fake.profile()
        self.profile_3 = fake.profile()

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

        self.user_3 = CustomUser.objects.create_user(
            username=self.profile_3.get("username"),
            password="demo_password",
            first_name=self.profile_3.get("name").split()[0],
            last_name=self.profile_3.get("name").split()[1],
            email=self.profile_3.get("mail"),
        )

        self.user_1_token = Token.objects.create(user=self.user_1)
        self.user_2_token = Token.objects.create(user=self.user_2)
        self.user_3_token = Token.objects.create(user=self.user_3)

        for _ in range(5):
            Tweet.objects.create(
                author=self.user_1,
                text=fake.paragraph(nb_sentences=2, variable_nb_sentences=False),
            )

        for _ in range(6):
            Tweet.objects.create(
                author=self.user_2,
                text=fake.paragraph(nb_sentences=2, variable_nb_sentences=False),
            )

        for _ in range(3):
            Tweet.objects.create(
                author=self.user_3,
                text=fake.paragraph(nb_sentences=2, variable_nb_sentences=False),
            )

        Follow.objects.create(source_user=self.user_1, destination_user=self.user_2)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_1_token.key)

    def tearDown(self) -> None:
        CustomUser.objects.all().delete()
        Token.objects.all().delete()
        Tweet.objects.all().delete()

    def test_newsfeed_success_response(self):
        response = self.client.get(self.newsfeed_url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="response status ok"
        )
        self.assertEqual(
            len(response.data.get("results")), 10, msg="default pagination ok"
        )
        self.assertEqual(response.data.get("count"), 11, msg="default pagination ok")

    def test_no_follower_user(self):
        """
        Test if user did not follow anybody
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_2_token.key)
        response = self.client.get(self.newsfeed_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="response status ok",
        )
        self.assertEqual(
            len(response.data.get("results")), 6, msg="default pagination ok"
        )
        self.assertEqual(response.data.get("count"), 6, msg="default pagination ok")
