import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


# Словарь для привязки моделей к csv-файлам
DATABASES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


# Создание команды
class Command(BaseCommand):
    # Описание команды
    help = 'Загружает данные из csv-файлов, расположенных в папке static/data.'

    def handle(self, *args, **options):
        # Цикл по всем моделям из словаря
        for model, csv_file in DATABASES_DICT.items():
            # Открытие csv-файла и чтение данных с использованием DictReader
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r',
                encoding='utf-8',
            ) as file:
                reader = csv.DictReader(file)
                # Цикл по строкам csv-файла,
                # создание или обновление экземпляра модели
                for data in reader:
                    model.objects.get_or_create(**data)
        # Вывод успешного завершения команды
        self.stdout.write(self.style.SUCCESS('Успешно заполнение базы.'))
