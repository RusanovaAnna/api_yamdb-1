from django.core.management.base import BaseCommand
from reviews import utils


class Command(BaseCommand):
    help = "Загружает в базу данных тестовые данные"

    def handle(self, *args, **kwargs):
        utils
