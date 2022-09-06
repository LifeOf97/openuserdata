from django.contrib.auth import get_user_model
from faker import Faker
import pytest
import random

# Faker
fake = Faker()
Faker.seed(0)


@pytest.fixture
def user():
    """
    User model as fixture
    """
    return get_user_model()


@pytest.fixture
def user_data_1():
    return dict(
        username=fake.user_name(),
        email=fake.safe_email(),
        app_name='my first app',
        password=fake.password(length=10)
    )


@pytest.fixture
def user_data_2():
    return dict(
        username=fake.user_name(),
        email=fake.safe_email(),
        cid=fake.ean(length=13),
        aid=fake.uuid4(),
        app_name="my first app",
        password=fake.password(length=10)
    )


@pytest.fixture
def create_mth(db, user, user_data_2):
    """
    Fixture to create a user with the object create method.
    """
    user = user.objects.create(**user_data_2)
    user.set_password(user_data_2['password'])
    user.save()
    return user


@pytest.fixture
def create_user_mth(db, user, user_data_1):
    """
    Fixture to create a new user with the create_user method
    """
    user = user.objects.create_user(**user_data_1)
    user.save()
    return user


@pytest.fixture
def create_superuser_mth(db, user, user_data_1):
    """
    Fixture to create a new superuser with the create_superuser method
    """
    user = user.objects.create_superuser(**user_data_1)
    user.save()
    return user


@pytest.fixture
def api_users(db, user):
    for _ in range(20):
        openuser = user.objects.create(
            cid=fake.ean(length=13),
            app_name=fake.first_name(),
            aid=fake.uuid4(),
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            other_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=99),
            about=fake.sentence(nb_words=25)
        )
        openuser.set_password(fake.password(length=10))
        openuser.save()


@pytest.fixture
def api_users_2(db, user):
    for _ in range(20):
        openuser = user.objects.create(
            cid="28757941857142064086",
            app_name="my first app",
            aid=fake.uuid4(),
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            other_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=99),
            about=fake.sentence(nb_words=25)
        )
        openuser.set_password(fake.password(length=10))
        openuser.save()


@pytest.fixture
def api_test_user():
    return dict(
        username=fake.unique.user_name(),
        email=fake.unique.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        other_name=fake.last_name(),
        gender=random.choice(['Male', 'Female']),
        dob=fake.date_of_birth(minimum_age=18, maximum_age=99),
        about=fake.sentence(nb_words=25),
        password=fake.password(length=10)
    )


@pytest.fixture
def api_test_user_2(db, user):
    data = dict(
        cid="28757941857142064086",
        app_name="my first app",
        aid=fake.uuid4(),
        username=fake.unique.user_name(),
        email=fake.unique.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        other_name=fake.last_name(),
        gender=random.choice(['Male', 'Female']),
        dob=fake.date_of_birth(minimum_age=18, maximum_age=99),
        about=fake.sentence(nb_words=25),
        password=fake.password(length=10)
    )
    openuser = user.objects.create(**data)
    openuser.set_password(data['password'])
    openuser.save()
    return data
