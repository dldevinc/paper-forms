from django import forms
from django.forms.renderers import Jinja2, DjangoTemplates

from paper_forms.composers.base import BaseComposer


class StringRendererComposer(BaseComposer):
    renderer = "django.forms.renderers.Jinja2"


class InstanceRendererComposer(BaseComposer):
    renderer = Jinja2()


def test_string_renderer():
    composer = StringRendererComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, Jinja2)


def test_instance_renderer():
    composer = InstanceRendererComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, Jinja2)


def test_default_renderer():
    composer = BaseComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, DjangoTemplates)
