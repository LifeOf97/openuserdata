from django.views.generic import RedirectView
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='api/')),
    path('api/', include("openuser.urls", namespace="v1"))
]
