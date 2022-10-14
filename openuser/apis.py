from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets, views
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.conf import settings
from django.http import Http404
from . import serializers
from . import filters


# Custom user model
User = get_user_model()


class APIRootView(views.APIView):

    @extend_schema(request=None, responses={200: None})
    def get(self, request):
        """
        Brief service details
        """
        data = {
            'Hello': 'Welcome to Open User Data REST API free service',
            'Home Page': 'https://openuser.xyz',
            'Documentations': {
                'REDOC': reverse('redoc', request=request),
                'SWAGGER': reverse('swagger-ui', request=request),
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OpenUserDataApiViewset(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for Openuserdata users. Comes with limited functionality.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.OpenUserDataserializer
    filterset_class = filters.UserFilter
    search_fields = ['=username', '=first_name', '=last_name', '=other_name']
    ordering_fields = ['username', 'email', 'dob']
    throttle_scope = 'anon'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_staff=False)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of users.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns an instance of a user.
        """
        return super().retrieve(request, *args, **kwargs)


class CreatorsOpenuserdataApiViewset(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.CreatorsOpenUserDataSerializer
    filterset_class = filters.UserFilter
    search_fields = ['=username', '=first_name', '=last_name', '=other_name']
    ordering_fields = ['username', 'email', 'dob']
    throttle_scope = 'creators'

    def get_permissions(self, *args, **kwargs):
        if self.action in ['create', 'list', 'retrieve', 'app_users_count']:
            permission_classes = [permissions.AllowAny, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset.filter(cid=self.kwargs['cid'], app_name=self.kwargs['app_name'], is_staff=False)

        if data.count() == 0:
            raise Http404
        return data

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()

        if 'users/me/' in self.request.path:
            obj = get_object_or_404(queryset, username=self.request.user.username)
        else:
            obj = get_object_or_404(queryset, username=self.kwargs['username'])

        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, cid=None, app_name=None, **kwargs):
        """
        Creates a new user profile in the current app instance.
        Returns the newly created users details.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})

        # get the app id
        app_id = User.objects.filter(cid=cid, app_name=app_name)[0].aid

        # make sure the creator making this request has not exceeded their users limit
        if self.get_queryset().count() < settings.MAX_NUMBER_OF_PROFILES:
            if serializer.is_valid():
                serializer.save(app_name=app_name, cid=cid, aid=app_id)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={'error': _(F'You have reached your open users limit ({settings.MAX_NUMBER_OF_PROFILES})')},
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        """
        Returns a list of users.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, username=None, *args, **kwargs):
        """
        Returns an instance of a user.

        Append to URL syntax: username
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, cid=None, app_name=None, username=None, **kwargs):
        """
        Updates user details in the current app instance.
        Returns the updated users detail.

        Append to URL syntax: creators_id/app_name/username
        """
        serializer = self.get_serializer(
            instance=self.get_object(), data=request.data,
            context={'request': request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(app_name=app_name, cid=cid)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, cid=None, app_name=None, username=None, **kwargs):
        """
        Deletes the currently logged in user from your app instance permanently.
        Returns deleted users detail.
        """
        if self.get_object():
            if self.get_queryset().count() > 2:
                user = self.get_object()
                app_name, username, email, uid = user.app_name, user.username, user.email, user.uid
                data = {
                    'uid': uid, 'username': username, 'app_name': app_name,
                    'email': email, 'detail': "Deleted successfuly"
                }
                user.delete()
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)

            return Response(
                data={'error': 'Cannot delete any more user, as every app instance must have atleast 2 active users'},
                status=status.HTTP_403_FORBIDDEN
            )

    # extra actions
    @action(detail=False, methods=['GET'],)
    def app_users_count(self, request, *args, **kwargs):
        """
        Returns the total number of users in your app.
        """
        return Response(
            data={'detail': self.get_queryset().count()},
            status=status.HTTP_200_OK
        )


class LoginSessionApiView(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.LoginSessionSerializer

    def post(self, request, *args, **kwargs):
        """
        Accepts the following post parameters: username/email and password, to
        login a user via session.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            if user is not None:
                login(request, user)
                response = Response(data={"detail": _("Logged in successfully")}, status=status.HTTP_200_OK)
                return response

            return Response(data={"detail": _("wrong username/email or password")}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutSessionApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    @extend_schema(parameters=None, request=None, responses={200: None})
    def post(self, request, *args, **kwargs):
        """
        Logs out a session authenticated user.
        """
        logout(request)
        return Response(data={"detail": _("Logged out successfully")}, status=status.HTTP_200_OK)
