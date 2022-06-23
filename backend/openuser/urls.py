from django.urls import path
from . import apis

app_name = 'v1'

urlpatterns = [
    # Creators openuserdata urls endpoint with full capabilities
    path(
        '<str:cid>/<str:app_name>/users/new/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'post': 'create'}),
        name='creators_users_create'
    ),
    path(
        '<str:cid>/<str:app_name>/users/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'list'}),
        name='creators_users_list'
    ),
    path(
        '<str:cid>/<str:app_name>/users/<str:username>/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'retrieve'}),
        name='creators_users_details'
    ),
    path(
        '<str:cid>/<str:app_name>/users/<str:username>/update/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'put': 'update', 'patch': 'update'}),
        name='creators_users_update'
    ),
    path(
        '<str:cid>/<str:app_name>/users/<str:username>/delete/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'delete': 'destroy'}),
        name='creators_users_delete'
    ),

    # openuserdata urls endpoint with limited capabilities
    path(
        'users/',
        apis.OpenUserDataApiViewset.as_view({'get': 'list'}),
        name='users-list'
    ),
    path(
        'users/<str:username>/',
        apis.OpenUserDataApiViewset.as_view({'get': 'retrieve'}),
        name='users-details'
    ),
]
