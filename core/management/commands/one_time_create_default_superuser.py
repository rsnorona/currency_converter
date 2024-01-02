from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
import dotenv

dotenv.load_dotenv()


class Command(BaseCommand):
    help = "Creates the default superuser with access to the admin panel."

    def handle(self, *args, **options):
        try:
            default_super_user = User.objects.create(
                username=os.getenv("DEFAULT_SUPERUSER_USERNAME"),
                first_name=os.getenv("DEFAULT_SUPERUSER_FIRST_NAME"),
                last_name=os.getenv("DEFAULT_SUPERUSER_LAST_NAME"),
                email=os.getenv("DEFAULT_SUPERUSER_EMAIL"),
                is_active=True,
                is_staff=True,
                is_superuser=True,
            )
            default_super_user.set_password(os.getenv("DEFAULT_SUPERUSER_PASSWORD"))
            default_super_user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created default superuser: {default_super_user.username}"
                )
            )
        except:
            pass
