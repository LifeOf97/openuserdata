from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


class TestOpenUserApiViewset:

    @pytest.mark.django_db
    def test_get_all_users_endpoint(self, user, api_users):
        assert user.objects.count() == 20

        client = APIClient()

        res = client.get(reverse('users_list_basic', kwargs={'version': 'v1'}), format='json')

        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 20

    @pytest.mark.django_db
    def test_get_a_specific_user_via_username(self, user, api_users):
        # because of the api_users fixture param
        assert user.objects.count() == 20

        client = APIClient()

        username = user.objects.all()[4].username

        res = client.get(
            reverse('users_detail_basic', kwargs={'version': 'v1', 'username': username}),
            format='json'
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data['username'] == username

    @pytest.mark.django_db
    def test_limit_and_offset_pagination_works_properly(self, user, api_users):
        assert user.objects.count() == 20

        client = APIClient()
        url = F"{reverse('users_list_basic', kwargs={'version': 'v1'})}?limit=5"

        res = client.get(url, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 20
        assert len(res.data['results']) == 5
