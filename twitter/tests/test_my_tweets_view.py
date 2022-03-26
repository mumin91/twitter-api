from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from applibs.fake import fake
from twitter.models import CustomUser, Tweet


class MyTweetsViewTest(APITestCase):
    def setUp(self) -> None:
        self.my_tweets_url = reverse("my_tweets")
        self.limit_offset = "?limit=2&offset=1"

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

        for _ in range(11):
            Tweet.objects.create(author=self.user_1, text=fake.paragraph(nb_sentences=2, variable_nb_sentences=False))

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_1_token.key)

    def tearDown(self) -> None:
        CustomUser.objects.all().delete()
        Token.objects.all().delete()
        Tweet.objects.all().delete()

    def test_my_tweets_success_response(self):
        response = self.client.get(self.my_tweets_url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="response status ok"
        )
        self.assertEqual(len(response.data.get("results")), 10, msg="default pagination ok")
        self.assertEqual(response.data.get("count"), 11, msg="default pagination ok")

    def test_no_tweet_response(self):
        """
        Test if user did not post any tweet yet
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_2_token.key)
        response = self.client.get(self.my_tweets_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="response status ok",
        )
        self.assertEqual(len(response.data.get("results")), 0, msg="default pagination ok")
        self.assertEqual(response.data.get("count"), 0, msg="default pagination ok")
        self.assertIsNone(response.data.get("next"))
        self.assertIsNone(response.data.get("previous"))
