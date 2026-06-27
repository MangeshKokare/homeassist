from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

from django.contrib.auth.models import User
from core.models import Profile
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        bot, created = User.objects.get_or_create(
            username="homeassist_bot",
            defaults={
                "first_name": "HomeAssist",
                "last_name": "Assistant",
            }
        )

        if created:
            bot.set_password("homeassist123")
            bot.save()

        Profile.objects.get_or_create(
            user=bot,
            defaults={
                "role": "provider",
                "phone": "9999999999",
                "address": "HomeAssist Support",
                "city": "Pune",
                "state": "Maharashtra",
                "pincode": "411001",
            }
        )

        self.stdout.write(
            self.style.SUCCESS("HomeAssist Bot Ready!")
        )