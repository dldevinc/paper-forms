from django import forms
from django.forms.renderers import Jinja2, TemplatesSetting

from paper_forms.composers.base import BaseComposer


class StringRendererComposer(BaseComposer):
    renderer = "django.forms.renderers.Jinja2"
    widgets = {
        "name": forms.CharField,
        "height": forms.IntegerField(),
    }


class InstanceRendererComposer(BaseComposer):
    renderer = Jinja2()


class TestRenderer:
    def test_composer_string_renderer(self):
        composer = StringRendererComposer()
        renderer = composer.get_renderer(forms.Form())
        assert isinstance(renderer, Jinja2)

    def test_composer_instance_renderer(self):
        composer = InstanceRendererComposer()
        renderer = composer.get_renderer(forms.Form())
        assert isinstance(renderer, Jinja2)

    def test_conf_renderer(self, paper_conf):
        paper_conf.DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

        composer = BaseComposer()
        renderer = composer.get_renderer(forms.Form())
        assert isinstance(renderer, TemplatesSetting)

    def test_composer_renderer_priority(self, paper_conf):
        # composer renderer have a higher priority than Django setting
        paper_conf.DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

        composer = StringRendererComposer()
        renderer = composer.get_renderer(forms.Form())
        assert isinstance(renderer, Jinja2)

    def test_empty_renderer(self):
        composer = BaseComposer()
        renderer = composer.get_renderer(forms.Form())
        assert renderer is None


class TestWidget:
    def test_attribute_class(self):
        composer = StringRendererComposer()
        widget = composer.get_widget("name")
        assert isinstance(widget, forms.CharField)

    def test_attribute_instance(self):
        composer = StringRendererComposer()
        widget = composer.get_widget("height")
        assert isinstance(widget, forms.IntegerField)

    def test_undefined(self):
        composer = StringRendererComposer()
        widget = composer.get_widget("age")
        assert widget is None
