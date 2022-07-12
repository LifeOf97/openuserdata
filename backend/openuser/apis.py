from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from . import serializers
from . import filters

# Custom user model
User = get_user_model()


class OpenUserDataApiViewset(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for Openuserdata users. Comes with limited functionality.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.OpenUserDataserializer
    filterset_class = filters.UserFilter
    search_fields = ['=username', '=first_name', '=last_name', '=other_name']
    ordering_fields = ['username', 'dob']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_staff=False)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True, context={'request': request})
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_object()), context={'request': request})
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)


class CreatorsOpenuserdataApiViewset(viewsets.GenericViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.CreatorsOpenUserDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(cid=self.kwargs['cid'], app_name=self.kwargs['app_name'], is_staff=False)

    def create(self, request, cid=None, app_name=None, **kwargs):
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
            data={'error': _('You have reached your open users limit')},
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, cid=None, app_name=None, **kwargs):
        """
        Returns a list of all users belongint to the current app instance
        """
        serializer = self.get_serializer(self.get_queryset(), many=True, context={'request': request})
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, cid=None, app_name=None, username=None, **kwargs):
        """
        Returns the details of the requested user in the current app instance.
        """
        serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, cid=None, app_name=None, username=None, **kwargs):
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

    def destroy(self, request, cid=None, app_name=None, username=None, **kwargs):
        """
        Deletes the currently logged in user from your app instance permanently.
        Returns deleted limited users detail.
        """
        openuser = self.get_object()
        app_name, username, uid = openuser.app_name, openuser.username, openuser.uid
        data = {'uid': uid, 'username': username, 'app_name': app_name, 'detail': "Deleted successfuly"}
        openuser.delete()
        return Response(data={'data': data}, status=status.HTTP_204_NO_CONTENT)
