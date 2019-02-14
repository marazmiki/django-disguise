import pytest


@pytest.fixture(autouse=True)
def autouse_db(db):
    "make use a database connection all over the test cases"
    pass


@pytest.fixture
def super_user(django_user_model):
    "creates a superuser instance"
    return django_user_model.objects.create_superuser(
        username='root',
        password='root',
        email='root@example.com'
    )


@pytest.fixture
def regular_user(django_user_model):
    "creates a regular user instance"
    return django_user_model.objects.create_user(
        username='user',
        password='user',
        email='user@example.com'
    )
