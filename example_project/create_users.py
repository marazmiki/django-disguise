import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_project.settings')

from django import setup
from django.contrib.auth import get_user_model

setup()

first_names = [
    'Charlie', 'Dennis', 'Dee', 'Frank', 'Ronald', 'Lyam', 'Margaret', 'Bill',
    'Barry', 'Michael', 'George', 'Buster', 'George Michael', 'Gob', 'Lucille',
]
last_names = [
    'Kelly', 'Reynolds', 'McDonald', 'McPoyle', 'Ponderosa',
    'Zuckerkorn', 'Bluth', 'Austero',
]


def user_exists(username):
    return get_user_model().objects.filter(username=username).exists()


def create_random_person():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    username = (first_name.lower() + '_' + last_name.lower()).replace(' ', '_')
    email = f'{username}@example.com'

    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
    }


def create_some_users(number):
    User = get_user_model()
    created = 0

    if not user_exists('admin'):
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
 
    while 42:
        row = create_random_person() 
        if not user_exists(row['username']):
            User.objects.create_user(**row)
            created += 1
        if created > number:
            break


if __name__ == '__main__':
    create_some_users(15)
