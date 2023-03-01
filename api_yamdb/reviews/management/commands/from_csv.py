import csv

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User
from reviews.models import (Title, Genre, Category,
                            Review, Comments)


class Command(BaseCommand):

    def handle(self, *args, **options):
        DIR_DATA = os.path.join(settings.BASE_DIR, 'static/data/')

        with open(DIR_DATA + 'users.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                """final = #тут то что ты импортировал.
                   Юзер запишу как пример и неазову юзер"""
                final = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                final.save()

        with open(DIR_DATA + 'category.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                final = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                final.save()

        with open(DIR_DATA + 'comments.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                final = Comments(
                    id=row['id'],
                    reviews=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                final.save()

        with open(DIR_DATA + 'genre_title.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.set([genre])
                title.save()

        with open(DIR_DATA + 'genre.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                final = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                final.save()

        with open(DIR_DATA + 'review.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                final = Title(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                final.save()

        with open(DIR_DATA + 'titles.csv', encoding='utf-8-sig') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                final = Title(
                    id=row['id'],
                    name=['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
                final.save()
