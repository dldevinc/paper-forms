from .views import DjangoView, JinjaView

try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url


app_name = "app"
urlpatterns = [
    url(r"^django/$", DjangoView.as_view(), name="django"),
    url(r"^jinja2/$", JinjaView.as_view(), name="jinja2"),
]
