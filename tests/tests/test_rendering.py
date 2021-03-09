import re

import django
import pytest
from django import forms
from django.template import engines


class SimpleForm(forms.Form):
    use_required_attribute = False

    name = forms.CharField()
    age = forms.IntegerField(
        min_value=18
    )
    birth = forms.DateField()
    email = forms.EmailField()
    photo = forms.ImageField()
    url = forms.URLField()
    color = forms.ChoiceField(
        choices=(
            ("r", "Red"),
            ("g", "Green"),
            ("b", "Blue"),
        )
    )
    terms = forms.BooleanField()


class TestDjangoTemplates:
    def setup_class(self):
        self.engine = engines["django"]

    def test_default_field_rendering(self):
        # без настроек, шаблонный тэг {% field %} рендерит стандартные виджеты
        default_template = self.engine.from_string(
            '<form method="post">'
            '{{ form.name }}'
            '{{ form.age }}'
            '{{ form.birth }}'
            '{{ form.email }}'
            '{{ form.photo }}'
            '{{ form.url }}'
            '{{ form.color }}'
            '{{ form.terms }}'
            '<button type="submit">Submit</button>'
            '</form>'
        )
        default_response = default_template.render({
            "form": SimpleForm()
        })

        paper_template = self.engine.from_string(
            '{% load paper_forms %}'
            '<form method="post">'
            '{% field form.name %}'
            '{% field form.age %}'
            '{% field form.birth %}'
            '{% field form.email %}'
            '{% field form.photo %}'
            '{% field form.url %}'
            '{% field form.color %}'
            '{% field form.terms %}'
            '<button type="submit">Submit</button>'
            '</form>'
        )
        paper_response = paper_template.render({
            "form": SimpleForm()
        })

        assert default_response == paper_response

    def test_additional_attributes(self):
        template = self.engine.from_string(
            '{% load paper_forms %}'
            '{% field form.name placeholder="Enter your name" %}'
        )
        response = template.render({
            "form": SimpleForm()
        })

        response = re.sub(r'\s/>', '>', response)
        assert response in {
            '<input type="text" name="name" placeholder="Enter your name" id="id_name">',
            '<input type="text" name="name" id="id_name" placeholder="Enter your name">'
        }

    def test_data_attributes(self):
        template = self.engine.from_string(
            '{% load paper_forms %}'
            '{% field form.name data__field__title="Enter your name" %}'
        )
        response = template.render({
            "form": SimpleForm()
        })

        response = re.sub(r'\s/>', '>', response)
        assert response in {
            '<input type="text" name="name" data-field-title="Enter your name" id="id_name">',
            '<input type="text" name="name" id="id_name" data-field-title="Enter your name">'
        }


class TestJinja2:
    @pytest.mark.parametrize("engine_name", ["jinja2", "django-jinja"])
    def test_jinja2_default_field_rendering(self, engine_name):
        engine = engines[engine_name]

        # без настроек, шаблонный тэг {% field %} рендерит стандартные виджеты
        default_template = engine.from_string(
            '<form method="post">'
            '{{ form.name }}'
            '{{ form.age }}'
            '{{ form.birth }}'
            '{{ form.email }}'
            '{{ form.photo }}'
            '{{ form.url }}'
            '{{ form.color }}'
            '{{ form.terms }}'
            '<button type="submit">Submit</button>'
            '</form>'
        )
        default_response = default_template.render({
            "form": SimpleForm()
        })

        paper_template = engine.from_string(
            '<form method="post">'
            '{% field form.name %}'
            '{% field form.age %}'
            '{% field form.birth %}'
            '{% field form.email %}'
            '{% field form.photo %}'
            '{% field form.url %}'
            '{% field form.color %}'
            '{% field form.terms %}'
            '<button type="submit">Submit</button>'
            '</form>'
        )
        paper_response = paper_template.render({
            "form": SimpleForm()
        })

        assert default_response == paper_response

    @pytest.mark.parametrize("engine_name", ["jinja2", "django-jinja"])
    def test_additional_attributes(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            '{% field form.name, placeholder="Enter your name" %}'
        )
        response = template.render({
            "form": SimpleForm()
        })

        response = re.sub(r'\s/>', '>', response)
        assert response in {
            '<input type="text" name="name" placeholder="Enter your name" id="id_name">',
            '<input type="text" name="name" id="id_name" placeholder="Enter your name">'
        }

    @pytest.mark.parametrize("engine_name", ["jinja2", "django-jinja"])
    def test_data_attributes(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            '{% field form.name, data__field__title="Enter your name" %}'
        )
        response = template.render({
            "form": SimpleForm()
        })

        response = re.sub(r'\s/>', '>', response)
        assert response in {
            '<input type="text" name="name" data-field-title="Enter your name" id="id_name">',
            '<input type="text" name="name" id="id_name" data-field-title="Enter your name">'
        }
