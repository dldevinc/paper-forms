from django import forms
from django.forms.renderers import Jinja2, TemplatesSetting

from paper_forms.composers.base import BaseComposer


class StringRendererComposer(BaseComposer):
    renderer = "django.forms.renderers.Jinja2"


class InstanceRendererComposer(BaseComposer):
    renderer = Jinja2()


def test_composer_string_renderer():
    composer = StringRendererComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, Jinja2)


def test_composer_instance_renderer():
    composer = InstanceRendererComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, Jinja2)


def test_conf_renderer(paper_conf):
    paper_conf.DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

    composer = BaseComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, TemplatesSetting)


def test_composer_renderer_priority(paper_conf):
    # composer renderer have a higher priority than Django setting
    paper_conf.DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

    composer = StringRendererComposer()
    renderer = composer.get_renderer(forms.Form())
    assert isinstance(renderer, Jinja2)


def test_empty_renderer():
    composer = BaseComposer()
    renderer = composer.get_renderer(forms.Form())
    assert renderer is None
