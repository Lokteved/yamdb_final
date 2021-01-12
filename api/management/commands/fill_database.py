import csv
import os

from django.core.management import BaseCommand
from django.db.models import Model

from api.models import (
    Category,
    Comments,
    Genre,
    GenreTitle,
    Review,
    Title,
    User
)

MAPPER = (
    ('users.csv', User),
    ('category.csv', Category),
    ('titles.csv', Title),
    ('review.csv', Review),
    ('comments.csv', Comments),
    ('genre.csv', Genre),
    ('genre_title.csv', GenreTitle)
)


class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def fill_model(self, file_name: str, model: Model):
        with open(os.path.join('data', file_name), 'r') as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                _, _ = model.objects.get_or_create(**row)

    def handle(self, *args, **kwargs):
        for case in MAPPER:
            self.fill_model(*case)
