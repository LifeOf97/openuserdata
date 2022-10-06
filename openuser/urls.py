from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path
from . import apis


urlpatterns = [
    # schema
    path('api/<version>/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/<version>/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/<version>/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # openuserdata urls endpoint with limited capabilities
    path(
        'api/<version>/users/',
        apis.OpenUserDataApiViewset.as_view({'get': 'list'}),
        name='users_list_basic'
    ),
    path(
        'api/<version>/users/<str:username>/',
        apis.OpenUserDataApiViewset.as_view({'get': 'retrieve'}),
        name='users_detail_basic'
    ),

    # Creators openuserdata urls endpoint with full capabilities
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'list'}),
        name='users_list'
    ),
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/new/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'post': 'create'}),
        name='users_create'
    ),
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/me/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'retrieve'}),
        name='users_details_authenticated'
    ),
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/me/update/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'put': 'update', 'patch': 'update'}),
        name='users_update_authenticated'
    ),
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/me/delete/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'delete': 'destroy'}),
        name='users_delete_authenticated'
    ),
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/count/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'app_users_count'}),
        name='users_count'
    ),
    path(
        'api/<version>/<str:cid>/<str:app_name>/app/users/<str:username>/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'retrieve'}),
        name='users_details_username'
    ),

    # user authentication urls endpoint
    path(
        "api/<version>/auth/login/token/",
        TokenObtainPairView.as_view(),
        name="login_via_token"
    ),
    path(
        "api/<version>/auth/refresh/token/",
        TokenRefreshView.as_view(),
        name="login_token_refresh"
    ),
    path(
        "api/<version>/auth/verify/token/",
        TokenVerifyView.as_view(),
        name="login_token_verify"
    ),
    path(
        "api/<version>/auth/login/session/",
        apis.LoginSessionApiView.as_view({'post': 'post'}),
        name="login_via_session"
    ),
    path(
        "api/<version>/auth/logout/session/",
        apis.LogoutSessionApiView.as_view(),
        name="logout_via_session"
    ),
]
