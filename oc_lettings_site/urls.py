from django.contrib import admin
from django.urls import path, include
from . import views


def trigger_error(request):
    1 / 0


urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include("lettings.urls")),
    path('profiles/', include("profiles.urls")),
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
]
