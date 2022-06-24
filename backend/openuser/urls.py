from django.urls import path
from . import apis


urlpatterns = [
    # Creators openuserdata urls endpoint with full capabilities
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/new/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'post': 'create'}),
        name='creators_users_create'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'list'}),
        name='creators_users_list'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/<str:username>/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'get': 'retrieve'}),
        name='creators_users_details'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/<str:username>/update/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'put': 'update', 'patch': 'update'}),
        name='creators_users_update'
    ),
    path(
        '<str:cid>/<str:app_name>/api/<version>/users/<str:username>/delete/',
        apis.CreatorsOpenuserdataApiViewset.as_view({'delete': 'destroy'}),
        name='creators_users_delete'
    ),

    # openuserdata urls endpoint with limited capabilities
    path(
        'api/<version>/users/',
        apis.OpenUserDataApiViewset.as_view({'get': 'list'}),
        name='users-list'
    ),
    path(
        'api/<version>/users/<str:username>/',
        apis.OpenUserDataApiViewset.as_view({'get': 'retrieve'}),
        name='users-details'
    ),
]
