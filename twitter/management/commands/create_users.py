from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from applibs.fake import fake
from twitter.models import CustomUser


class Command(BaseCommand):
    help = "Create Dummy Users"

    def handle(self, *args, **options):
        for i in range(5):
            profile = fake.profile()
            name_list = profile.get("name").split()

            user = CustomUser.objects.create_user(
                username=profile.get("username"),
                password="demo_password",
                first_name=name_list[0],
                last_name=name_list[1],
                email=profile.get("mail"),
            )
            Token.objects.create(user=user)

            data = {
                "id": user.pk,
                "username": user.username,
                "password": "demo_password",
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }

            self.stdout.write(f"USER {i + 1} CREATED WITH FOLLOWING DETAILS:")
            self.stdout.write(repr(data))
            self.stdout.write("\n")
