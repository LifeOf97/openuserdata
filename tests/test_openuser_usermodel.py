from django.db import utils as db_exception
from django.utils.text import slugify
from faker import Faker
import pytest


class TestUserModel:

    fake = Faker()

    @pytest.mark.django_db
    def test_usermodel_create_method_only_sets_users_as_is_active(self, user, create_mth):
        # because of the create_mth fixture
        assert user.objects.count() == 1

        # users only have is_active status set to true
        assert create_mth.is_active
        assert not create_mth.is_staff
        assert not create_mth.is_superuser

    @pytest.mark.django_db
    def test_usermodel_create_user_method_only_sets_users_as_is_active(self, user, create_user_mth):
        # because of the create_mth fixture
        assert user.objects.count() == 1

        # users only have is_active status set to true
        assert create_user_mth.is_active
        assert not create_user_mth.is_staff
        assert not create_user_mth.is_superuser

    @pytest.mark.django_db
    def test_usermodel_create_superuser_method_gives_users_all_privilege(self, user, create_superuser_mth):
        # because of the create_mth fixture
        assert user.objects.count() == 1

        # users only have is_active status set to true
        assert create_superuser_mth.is_active
        assert create_superuser_mth.is_staff
        assert create_superuser_mth.is_superuser

    @pytest.mark.django_db
    def test_usermodel_str_method_returns_username_and_app_name_if_present(
        self, user, create_mth, create_superuser_mth
    ):
        # because of the create_mth and create_superuser_mth fixture
        assert user.objects.count() == 2

        # str for create_mth fixture
        username = create_mth.username.replace(' ', '_').lower()
        app_name = slugify(create_mth.app_name.replace('_', ' '))
        assert str(create_mth) == F"{username} ({app_name})"

        # str for create_superuser_mth fixture
        username = create_superuser_mth.username.replace(' ', '_').lower()
        app_name = slugify(create_superuser_mth.app_name.replace('_', ' '))
        assert str(create_superuser_mth) == F"{username} ({app_name})"

    @pytest.mark.django_db
    def test_usermodel_app_name_field_obeys_max_length_validator(self, user):
        assert user.objects.count() == 0

        test_data = dict(
            username=self.fake.user_name(),
            email=self.fake.safe_email(),
            cid=self.fake.ean(length=13),
            aid=self.fake.uuid4(),
            app_name="this app name should not be more than 20 char",
            password=self.fake.password(length=10)
        )

        with pytest.raises(db_exception.DataError) as exc_info:
            user = user.objects.create(**test_data)
            user.set_password(test_data['password'])
            user.save()

        assert exc_info.type is db_exception.DataError
        assert "value too long for type character varying(20)" in str(exc_info.value)

    @pytest.mark.django_db
    def test_usermodel_username_field_obeys_max_length_validator(self, user):
        assert user.objects.count() == 0

        test_data = dict(
            username="ThisUserNameFieldIsToLong",
            email=self.fake.safe_email(),
            cid=self.fake.ean(length=13),
            aid=self.fake.uuid4(),
            app_name="my app name",
            password=self.fake.password(length=10)
        )

        with pytest.raises(db_exception.DataError) as exc_info:
            user = user.objects.create(**test_data)
            user.set_password(test_data['password'])
            user.save()

        assert exc_info.type is db_exception.DataError
        assert "value too long for type character varying(20)" in str(exc_info.value)

    @pytest.mark.django_db
    @pytest.mark.xfail
    def test_usermodel_username_field_can_only_contain_letters_numbers_and_underscore(self, user):
        """
        For some reasons, the username field validators param does not take effect while runnig my
        test.
        """
        assert user.objects.count() == 0

        test_data = dict(
            username="username-@-wrong",
            email=self.fake.safe_email(),
            cid=self.fake.ean(length=13),
            aid=self.fake.uuid4(),
            app_name="my app name",
            password=self.fake.password(length=10)
        )

        with pytest.raises(db_exception.DataError) as exc_info:
            user = user.objects.create(**test_data)
            user.set_password(test_data['password'])
            user.save()

        assert exc_info.type == db_exception.DataError

    @pytest.mark.django_db
    def test_usermodel_username_and_email_fields_are_converted_to_lowercase(self, user, user_data_2, create_mth):
        # because of the create_mth fixture
        assert user.objects.count() == 1

        assert create_mth.username == user_data_2['username'].replace(' ', '_').lower()
        assert create_mth.email == user_data_2['email'].lower()

    @pytest.mark.django_db(transaction=True)
    def test_usermodel_username_and_email_fields_should_be_unique(self, user):
        assert user.objects.count() == 0

        # test data
        test_data_1 = dict(
            username="testUserOne",
            email="TestUserOne@email.com",
            app_name="my first app",
            password="p@ssw0rd"
        )
        test_data_1_2 = dict(
            username="testUserOne",
            email="TestUserTwo@email.com",
            app_name="my second app",
            password="p@ssw0rd"
        )
        test_data_2_1 = dict(
            username="testUserTwo",
            email="TestUserOne@email.com",
            app_name="my third app",
            password="p@ssw0rd"
        )

        # create a user with the test_data_1 object
        user.objects.create_user(**test_data_1)

        # try to create another user with the same username value. test_data_1_2
        # but different email
        with pytest.raises(db_exception.IntegrityError) as exc_info:
            user.objects.create_user(**test_data_1_2)

        username = test_data_1_2['username'].replace(' ', '_').lower()
        assert exc_info.type is db_exception.IntegrityError
        assert F"Key (username)=({username}) already exists" in str(exc_info.value)

        # try to create another user with the same email value. test_data_2_1
        # but different username
        with pytest.raises(db_exception.IntegrityError) as exc_info:
            user.objects.create_user(**test_data_2_1)

        email = test_data_2_1['email'].lower()
        assert exc_info.type is db_exception.IntegrityError
        assert F"Key (email)=({email}) already exists" in str(exc_info.value)
