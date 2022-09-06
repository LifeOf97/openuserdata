from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path
from . import apis


urlpatterns = [
    # Creators openuserdata urls endpoint with full capabilities
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'list'}),
        name='users_list'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/add/user/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'post': 'create'}),
        name='users_create'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/<str:username>/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'retrieve'}),
        name='users_details_username'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/app/i/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'retrieve'}),
        name='users_details_authenticated'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/app/i/update/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'put': 'update', 'patch': 'update'}),
        name='users_update_authenticated'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/app/i/delete/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'delete': 'destroy'}),
        name='users_delete_authenticated'
    ),

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

    # user authentication urls endpoint
    path(
        "api/<version>/auth/login/token/",
        TokenObtainPairView.as_view(),
        name="login_via_token"
    ),
    path(
        "api/<version>/auth/verify/token/",
        TokenVerifyView.as_view(),
        name="login_token_verify"
    ),
    path(
        "api/<version>/auth/refresh/token/",
        TokenRefreshView.as_view(),
        name="login_token_refresh"
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
