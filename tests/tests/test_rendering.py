import pytest
from django import forms
from django.core.validators import MinValueValidator
from django.template import engines

from paper_forms.composer import BaseComposer


class BookForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100
    )
    author = forms.CharField(
        label="Author",
        max_length=50
    )
    pages = forms.IntegerField(
        label="Number of Pages",
        validators=[MinValueValidator(1)]
    )

    class Composer(BaseComposer):
        template_names = {
            "author": "fields/field.html",
            "pages": "fields/field.html",
        }


@pytest.mark.parametrize("engine_name", ["django"])
class TestDjango:
    def test_attribute(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.title placeholder=\"Book Title\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<input type="text" name="title" maxlength="100" placeholder="Book Title" '
            'required id="id_title">'
        )

    def test_data_attribute(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.title data__field__id=\"42\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<input type="text" name="title" maxlength="100" data-field-id="42" '
            'required id="id_title">'
        )

    def test_context_variable(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.author _style=\"dark\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<div class="field--dark">\n'
            '  <label for="id_author">Author</label>\n'
            '  <input type="text" name="author" maxlength="50" required id="id_author">\n\n\n'
            '</div>'
        )

    def test_special_cases(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.pages label=\"Page count\" help_text=\"Enter page count\" css_classes=\"field--large\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<div class="field--large">\n'
            '  <label for="id_pages">Page count</label>\n'
            '  <input type="number" name="pages" required id="id_pages">\n\n\n'
            '  <small>Enter page count</small>\n'
            '</div>'
        )


@pytest.mark.parametrize("engine_name", ["jinja2", "django-jinja"])
class TestJinja2:
    def test_attribute(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.title, placeholder=\"Book Title\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<input type="text" name="title" maxlength="100" placeholder="Book Title" '
            'required id="id_title">'
        )

    def test_data_attribute(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.title, data__field__id=\"42\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<input type="text" name="title" maxlength="100" data-field-id="42" '
            'required id="id_title">'
        )

    def test_context_variable(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.author, _style=\"dark\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<div class="field--dark">\n'
            '  <label for="id_author">Author</label>\n'
            '  <input type="text" name="author" maxlength="50" required id="id_author">\n\n\n'
            '</div>'
        )

    def test_special_cases(self, engine_name):
        engine = engines[engine_name]

        template = engine.from_string(
            "{% field form.pages, label=\"Page count\", help_text=\"Enter page count\", css_classes=\"field--large\" %}"
        )
        assert template.render({
            "form": BookForm()
        }) == (
            '<div class="field--large">\n'
            '  <label for="id_pages">Page count</label>\n'
            '  <input type="number" name="pages" required id="id_pages">\n\n\n'
            '  <small>Enter page count</small>\n'
            '</div>'
        )
