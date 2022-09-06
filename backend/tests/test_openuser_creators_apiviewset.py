from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


class TestOpenUserCreatorApiViewset:

    @pytest.mark.django_db
    def test_get_all_users_via_creators_endpoint(self, user, api_users_2):
        # because of the api_users_2 fixture param
        assert user.objects.count() == 20

        openuser = user.objects.all()[0]
        client = APIClient()
        res = client.get(
            reverse(
                "users_list",
                kwargs={
                    'version': 'v1',
                    'cid': openuser.cid,
                    'app_name': openuser.app_name
                }
            ),
            format='json',
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 20

    @pytest.mark.django_db
    def test_get_a_specific_user_via_username_on_creators_endpoint(self, user, api_users_2):
        # because of the api_users_2 fixture param
        assert user.objects.count() == 20

        openuser = user.objects.all()[5]

        client = APIClient()
        res = client.get(
            reverse(
                "users_details_username",
                kwargs={
                    'version': 'v1',
                    'cid': openuser.cid,
                    'app_name': openuser.app_name,
                    'username': openuser.username
                }
            ),
            format='json',
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data['username'] == openuser.username
        assert res.data['email'] == openuser.email
        assert res.data['app_name'] == openuser.app_name
        assert res.data['cid'] == openuser.cid
        assert res.data['uid'] == openuser.uid

    @pytest.mark.django_db
    def test_create_new_user_via_creators_endpoint(self, user, api_users_2, api_test_user):
        # because of the api_users_2 fixture param
        assert user.objects.count() == 20

        openuser = user.objects.all()[0]
        client = APIClient()
        res = client.post(
            reverse(
                "users_create",
                kwargs={'version': 'v1', 'cid': openuser.cid, 'app_name': openuser.app_name}
            ),
            data=api_test_user,
            format='json',
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert user.objects.count() == 21
        assert res.data['username'] == api_test_user['username']

    @pytest.mark.django_db
    def test_creator_users_can_login_via_token(self, user, api_users_2, api_test_user_2):
        # because of the api_users_2 and api_test_user_2 fixtures param
        assert user.objects.count() == 21

        client = APIClient()

        # now login the newly created user
        res = client.post(
            reverse('login_via_token', kwargs={'version': 'v1'}),
            data={'username': api_test_user_2['username'], 'password': api_test_user_2['password']},
            forma='json'
        )
        assert res.status_code == status.HTTP_200_OK
        assert 'access' in res.data
        assert 'refresh' in res.data

    @pytest.mark.django_db
    def test_authenticated_user_can_get_their_data_via_a_specific_endoint(self, user, api_test_user_2):
        # because of the api_test_user_2 fixture param
        assert user.objects.count() == 1

        openuser = user.objects.get(username=api_test_user_2['username'])
        client = APIClient()
        res = client.post(
            reverse('login_via_token', kwargs={'version': 'v1'}),
            data={'username': api_test_user_2['username'], 'password': api_test_user_2['password']},
            forma='json'
        )
        assert res.status_code == status.HTTP_200_OK

        # provide bearer token to authenticate subsequent request
        client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
        res = client.get(
            reverse(
                'users_details_authenticated',
                kwargs={
                    'version': 'v1',
                    'cid': openuser.cid,
                    'app_name': openuser.app_name
                }
            ),
            format='json',
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data['username'] == openuser.username
        assert res.data['uid'] == openuser.uid
        assert res.data['cid'] == openuser.cid
        assert res.data['app_name'] == openuser.app_name

    @pytest.mark.django_db
    def test_authenticated_users_can_update_their_data(self, user, api_test_user_2):
        # because of the api_test_user_2 fixture param
        assert user.objects.count() == 1

        openuser = user.objects.get(username=api_test_user_2['username'])
        client = APIClient()
        res = client.post(
            reverse('login_via_token', kwargs={'version': 'v1'}),
            data={'username': api_test_user_2['username'], 'password': api_test_user_2['password']},
            forma='json'
        )
        assert res.status_code == status.HTTP_200_OK

        # provide bearer token to authenticate subsequent request
        client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")

        # update authenticated user data
        new_data = dict(username='updated_username')

        res = client.put(
            reverse(
                'users_update_authenticated',
                kwargs={
                    'version': 'v1',
                    'cid': openuser.cid,
                    'app_name': openuser.app_name
                }
            ),
            data=new_data,
            format='json'
        )

        assert res.status_code == status.HTTP_202_ACCEPTED
        assert res.data['username'] != openuser.username
        assert res.data['username'] == new_data['username']

    @pytest.mark.django_db
    def test_creators_cannot_delete_app_users_if_users_is_less_than_3(self, user, api_test_user_2):
        # because of the api_test_user_2 fixture param
        assert user.objects.count() == 1

        openuser = user.objects.get(username=api_test_user_2['username'])
        client = APIClient()
        res = client.post(
            reverse('login_via_token', kwargs={'version': 'v1'}),
            data={'username': api_test_user_2['username'], 'password': api_test_user_2['password']},
            forma='json'
        )
        assert res.status_code == status.HTTP_200_OK

        # provide bearer token to authenticate subsequent request
        client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")

        res = client.delete(
            reverse(
                'users_delete_authenticated',
                kwargs={
                    'version': 'v1',
                    'cid': openuser.cid,
                    'app_name': openuser.app_name
                }
            ),
            format='json'
        )

        assert res.status_code == status.HTTP_403_FORBIDDEN
        assert user.objects.count() == 1
        assert str(res.data['error']).startswith('Cannot delete any more user')

    @pytest.mark.django_db
    def test_creators_can_delete_app_users_if_users_is_more_than_2(self, user, api_users_2, api_test_user_2):
        # because of api_users_2 and api_test_user_2 fixture param
        assert user.objects.count() == 21

        openuser = user.objects.get(username=api_test_user_2['username'])
        client = APIClient()
        res = client.post(
            reverse('login_via_token', kwargs={'version': 'v1'}),
            data={'username': api_test_user_2['username'], 'password': api_test_user_2['password']},
            forma='json'
        )
        assert res.status_code == status.HTTP_200_OK

        # provide bearer token to authenticate subsequent request
        client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")

        res = client.delete(
            reverse(
                'users_delete_authenticated',
                kwargs={
                    'version': 'v1',
                    'cid': openuser.cid,
                    'app_name': openuser.app_name
                }
            ),
            format='json'
        )

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert user.objects.count() == 20
        assert res.data['uid'] == openuser.uid
        assert res.data['username'] == openuser.username
        assert res.data['email'] == openuser.email
        assert res.data['app_name'] == openuser.app_name
        assert res.data['detail'] == 'Deleted successfuly'
