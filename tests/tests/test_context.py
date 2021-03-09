from django import forms

from paper_forms.composers.bootstrap4 import Bootstrap4

from .utils import get_bound_field


class SimpleForm(forms.Form):
    name = forms.CharField()


class BootstrapForm(forms.Form):
    name = forms.CharField()

    class Composer(Bootstrap4):
        labels = {
            "name": "Your name"
        }
        help_texts = {
            "name": "Enter your name"
        }


class TestSimpleFormContext:
    def setup_class(self):
        form = SimpleForm({
            "name": "Joe"
        })
        bf = get_bound_field(form, "name")
        self.context = bf.get_context(bf.widget)

    def test_errors(self):
        assert "errors" in self.context
        assert self.context["errors"] == []

    def test_label(self):
        assert "label" in self.context
        assert self.context["label"] == "Name"

    def test_help_text(self):
        assert "help_text" in self.context
        assert self.context["help_text"] == ""

    def test_widget(self):
        assert "widget" in self.context
        assert isinstance(self.context["widget"], dict)


class TestBootstrapFormContext:
    def setup_class(self):
        form = BootstrapForm({
            "name": "Joe"
        })
        bf = get_bound_field(form, "name")
        self.context = bf.get_context(bf.widget)

    def test_label(self):
        assert "label" in self.context
        assert self.context["label"] == "Your name"

    def test_help_text(self):
        assert "help_text" in self.context
        assert self.context["help_text"] == "Enter your name"
