from django.test import TestCase

from applibs.fake import fake
from twitter.models import CustomUser, Follow


class FollowTestCase(TestCase):
    def setUp(self):
        profiles = [fake.profile() for _ in range(3)]

        self.user_1 = CustomUser.objects.create_user(
            username=profiles[0].get("username"),
            password="demo_password",
            first_name=profiles[0].get("name").split()[0],
            last_name=profiles[0].get("name").split()[1],
            email=profiles[0].get("mail"),
        )

        self.user_2 = CustomUser.objects.create_user(
            username=profiles[1].get("username"),
            password="demo_password",
            first_name=profiles[1].get("name").split()[0],
            last_name=profiles[1].get("name").split()[1],
            email=profiles[1].get("mail"),
        )

        self.user_3 = CustomUser.objects.create_user(
            username=profiles[2].get("username"),
            password="demo_password",
            first_name=profiles[2].get("name").split()[0],
            last_name=profiles[2].get("name").split()[1],
            email=profiles[2].get("mail"),
        )

        Follow.objects.create(source_user=self.user_1, destination_user=self.user_2)
        Follow.objects.create(source_user=self.user_1, destination_user=self.user_3)

    def test_get_followed_ids(self):
        ids = Follow.objects.get_followed_ids(source_user_id=self.user_1.id)

        self.assertEqual(ids.__len__(), 2)

    def test_get_followed_ids_nil(self):
        ids = Follow.objects.get_followed_ids(source_user_id=self.user_2.id)

        self.assertIs(ids.__len__(), 0)

    def test_get_followed_ids_exception(self):
        ids = Follow.objects.get_followed_ids(source_user_id="id")

        self.assertIsNone(ids)

