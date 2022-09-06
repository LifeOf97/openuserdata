from django.db import utils as db_exception
from openuser.models import OpenuserCreator
from faker import Faker
import pytest


class TestOpenUserCreatorModel:

    fake = Faker()

    @pytest.mark.parametrize(
        "cid, username, max",
        [
            (
                F"{fake.ean(length=13)}{fake.ean(length=13)}",
                fake.user_name(),
                20
            ),
            (
                F"{fake.ean(length=13)}",
                "this_username_is_more_than_15_chars",
                15
            ),
        ]
    )
    @pytest.mark.django_db
    def test_openusercreatormodel_cid_field_obeys_the_max_length_validator(self, cid, username, max):
        with pytest.raises(db_exception.DataError) as exc_info:
            creator = OpenuserCreator.objects.create(cid=cid, username=username)
            creator.save()

        assert exc_info.type is db_exception.DataError
        assert F"value too long for type character varying({max})" in str(exc_info.value)
