from django.contrib import admin
from django.views.generic import RedirectView

try:
    from django.urls import include
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import include, url


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", RedirectView.as_view(pattern_name="app:django")),
    url(r"", include("app.urls")),
]
