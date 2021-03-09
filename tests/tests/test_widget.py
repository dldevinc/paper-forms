from django import forms

from paper_forms.composers.bootstrap4 import Bootstrap4

from ._models import SampleModel
from .utils import get_bound_field


class SampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    website = forms.URLField(
        widget=forms.TextInput
    )

    class Composer(Bootstrap4):
        widgets = {
            "website": forms.HiddenInput
        }


class SampleModelForm(forms.ModelForm):
    class Meta:
        model = SampleModel
        fields = forms.ALL_FIELDS
        widgets = {
            "password": forms.PasswordInput,
            "website": forms.HiddenInput,
        }

    class Composer(Bootstrap4):
        widgets = {
            "website": forms.TextInput,
        }


def test_default_widget():
    # Форма без composer'а использует стандартные виджеты.
    form = SampleForm()
    bf = get_bound_field(form, "name")
    assert type(bf.widget) is forms.TextInput

    model_form = SampleModelForm({})
    model_bf = get_bound_field(model_form, "name")
    assert type(model_bf.widget) is forms.TextInput


def test_form_widget():
    # Проверка возможности задать виджет в поле формы
    form = SampleForm()
    bf = get_bound_field(form, "password")
    assert type(bf.widget) is forms.PasswordInput


def test_composer_widget():
    # Виджет, заданный полем composer'а имеет наивысший приоритет
    form = SampleForm()
    bf = get_bound_field(form, "website")
    assert type(bf.widget) is forms.HiddenInput


def test_modelform_meta_widget():
    # Проверка возможности задать виджет в Meta-классе ModelForm
    form = SampleModelForm()
    bf = get_bound_field(form, "password")
    assert type(bf.widget) is forms.PasswordInput


def test_modelform_composer_widget():
    # Виджет, заданный полем composer'а имеет наивысший приоритет (в ModelForm)
    form = SampleModelForm()
    bf = get_bound_field(form, "website")
    assert type(bf.widget) is forms.TextInput
