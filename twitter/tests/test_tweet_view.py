from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token

from twitter.models import CustomUser, Tweet

fake = Faker()
from rest_framework.test import APITestCase


class TweetViewTest(APITestCase):
    def setUp(self) -> None:
        self.tweet_url = reverse("tweet")

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
        Tweet.objects.all().delete()

    def test_follow_success_response(self):
        payload = {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}

        response = self.client.post(self.tweet_url, payload, format="json")

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg="response status ok"
        )
        self.assertEqual(response.data, payload, msg="response body ok")

    def test_tweet_model_after_success_response(self):
        payload = {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}
        _ = self.client.post(self.tweet_url, payload, format="json")

        tweet_objs = Tweet.objects.all()

        self.assertGreater(tweet_objs.count(), 0, msg="single object created")
        self.assertEqual(tweet_objs.count(), 1, msg="single object created")
        self.assertLess(tweet_objs.count(), 2, msg="single object created")

        tweet_obj = tweet_objs[0]

        self.assertEqual(tweet_obj.author.id, self.user_1.id)
        self.assertEqual(tweet_obj.text, tweet_obj["text"])

    def test_tweet_validation_error_response(self):
        payload = {
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque sollicitudin aliquet nibh eget dignissim. Sed quis imperdiet ipsum. Suspendisse vel porta ex. Donec eu eros consequat, hendrerit erat et, condimentum augue. Sed accumsan mattis ante, id tempus lacus consectetur quis. In sed ultrices arcu. Maecenas quis sollicitudin neque. Vivamus suscipit elit nec venenatis bibendum. Vestibulum est nunc, sagittis eget placerat eget, venenatis et sem. Phasellus id tempor augue, porttitor fermentum nunc. Pellentesque quis arcu commodo mauris iaculis imperdiet sit amet elementum diam. Fusce id libero vehicula, convallis sem quis, mollis ligula. Pellentesque tincidunt, elit sit amet pharetra dignissim, dolor enim dignissim lorem, vel viverra lacus ligula a nunc. Maecenas varius pellentesque mattis."
        }
        error_response = {
            "text": ["Ensure this field has no more than 280 characters."]
        }

        response = self.client.post(self.tweet_url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="failed response status ok",
        )
        self.assertEqual(response.data, error_response, msg="error response body ok")
