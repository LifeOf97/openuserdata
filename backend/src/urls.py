from django.views.generic import RedirectView
from django.urls import path, include
from openuser.admin import admin_site
# from django.contrib import admin


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', RedirectView.as_view(url='api/')),
    path('api/', include("openuser.urls", namespace="v1"))
]
