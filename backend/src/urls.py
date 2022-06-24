from django.urls import path, include
from openuser.admin import admin_site
# from django.contrib import admin


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include("openuser.urls"))
]
