from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.conf import settings
from . import serializers

# Custom user model
User = get_user_model()


class OpenUserDataApiViewset(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for Openuserdata users. Comes with limited functionality.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.OpenUserDataserializer


class CreatorsOpenuserdataApiViewset(viewsets.GenericViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.CreatorsOpenUserDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(cid=self.kwargs['cid'], app_name=self.kwargs['app_name'])

    def create(self, request, cid=None, app_name=None):
        """
        Creates a new user profile in the current app instance.
        Returns the newly created users details.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})

        # make sure the creator making this request has not exceeded their users limit
        if self.get_queryset.count() < settings.MAX_NUMBER_OF_PROFILES:
            if serializer.is_valid():
                serializer.save()
                return Response(data={'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={'error': _('You have reached your Open users limit')},
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, cid=None, app_name=None):
        """
        Returns a list of all users belongint to the current app instance
        """
        serializer = self.get_serializer(self.get_queryset(), many=True, context={'request': request})
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, cid=None, app_name=None, username=None):
        """
        Returns the details of the requested user in the current app instance.
        """
        serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, cid=None, app_name=None, username=None):
        """
        Updates a user details in the current app instance.
        Returns the updated users detail.
        """
        serializer = self.get_serializer(
            instance=self.get_object(), data=request.data,
            context={'request': request}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(data={'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, cid=None, app_name=None, username=None):
        """
        Deletes the currently logged in user from your app instance permanently.
        Returns deleted limited users detail.
        """
        openuser = self.get_object()
        app_name, username, uid = openuser.app_name, openuser.username, openuser.uid
        data = {'uid': uid, 'username': username, 'app_name': app_name, 'detail': "Deleted successfuly"}
        openuser.delete()
        return Response(data={'data': data}, status=status.HTTP_204_NO_CONTENT)
