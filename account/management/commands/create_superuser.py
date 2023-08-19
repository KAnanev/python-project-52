from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import os


def get_env(key):
    value = os.getenv(key=key)
    if value is None:
        raise KeyError(f'Отсутствует переменная {key}!')
    return value


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):

        try:
            User.objects.create_superuser(
                username=get_env('DJANGO_SUPERUSER'),
                email=get_env('DJANGO_SUPERUSER_EMAIL'),
                password=get_env('DJANGO_SUPERUSER_PASS'),
            )

            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))

        except KeyError as er:
            self.stderr.write(self.style.ERROR(f"Произошла ошибка: {str(er)}\n"))

        except IntegrityError:
            self.stdout.write(self.style.WARNING('Superuser already created!'))
