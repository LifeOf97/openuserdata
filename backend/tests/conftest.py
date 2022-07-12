from django.contrib.auth import get_user_model
from faker import Faker
import pytest

# Faker
fake = Faker()
Faker.seed(0)


@pytest.fixture
def user_model():
    """
    User model as fixture
    """
    return get_user_model()


@pytest.fixture
def user_data_1():
    return dict(
        username=fake.user_name(),
        email=fake.safe_email(),
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
def create_mth(db, user_model, user_data_2):
    """
    Fixture to create a user with the object create method.
    """
    user = user_model.objects.create(**user_data_2)
    user.set_password(user_data_2['password'])
    user.save()
    return user


@pytest.fixture
def create_user_mth(db, user_model, user_data_1):
    """
    Fixture to create a new user with the create_user method
    """
    user = user_model.objects.create_user(**user_data_1)
    user.save()
    return user


@pytest.fixture
def create_superuser_mth(db, user_model, user_data_1):
    """
    Fixture to create a new user with the create_superuser method
    """
    user = user_model.objects.create_superuser(**user_data_1)
    user.save()
    return user
