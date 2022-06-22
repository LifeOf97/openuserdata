from django.views.generic import RedirectView
from django.urls import path, include
from openuser.admin import admin_site
# from django.contrib import admin


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', RedirectView.as_view(url='api/v1/')),
    path('api/v1/', include("openuser.urls", namespace="v1"))
]
