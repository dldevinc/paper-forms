from django import forms

from paper_forms.composers.bootstrap4 import Bootstrap4

from .utils import get_bound_field


class SimpleForm(forms.Form):
    name = forms.CharField()


class BootstrapForm(forms.Form):
    name = forms.CharField()
    over_18 = forms.BooleanField()
    gender = forms.ChoiceField(choices=(
        ("m", "Male"),
        ("f", "Female"),
    ))
    day = forms.TypedChoiceField(
        coerce=int,
        choices=(
            (0, "Mon"),
            (1, "Tue"),
            (2, "Wed"),
            (3, "Thu"),
            (4, "Fri"),
            (5, "Sat"),
            (6, "Sun"),
        ),
        widget=forms.CheckboxSelectMultiple
    )
    photo = forms.ImageField()

    class Composer(Bootstrap4):
        pass


class CustomForm(forms.Form):
    name = forms.CharField()
    over_18 = forms.BooleanField()
    gender = forms.ChoiceField(choices=(
        ("m", "Male"),
        ("f", "Female"),
    ))

    class Composer(Bootstrap4):
        widgets = {
            "gender": forms.RadioSelect,
        }


def test_empty_css_classes():
    # Форма без composer'а не добавляет никаких классов
    form = SimpleForm({})
    bf = get_bound_field(form, "name")
    assert "class" not in bf.get_widget_attrs(bf.widget)


def test_default_composer_css_classes():
    # Классы, добавляемые в методе `get_default_css_classes` composer'a
    form = BootstrapForm({})

    input_bf = get_bound_field(form, "name")
    assert input_bf.get_widget_attrs(input_bf.widget)["class"] == "form-control"

    checkbox_bf = get_bound_field(form, "over_18")
    assert checkbox_bf.get_widget_attrs(checkbox_bf.widget)["class"] == "form-check-input"

    select_bf = get_bound_field(form, "gender")
    assert select_bf.get_widget_attrs(select_bf.widget)["class"] == "custom-select"

    checkbox_select_bf = get_bound_field(form, "day")
    assert checkbox_select_bf.get_widget_attrs(checkbox_select_bf.widget)["class"] == "form-check-input"

    file_bf = get_bound_field(form, "photo")
    assert file_bf.get_widget_attrs(file_bf.widget)["class"] == "custom-file-input"


def test_explicit_css_classes():
    # Если в шаблонном тэге указаны CSS-классы, то они используются вместо
    # классов, добавляемых в методе `get_default_css_classes` composer'a.
    form = BootstrapForm({})
    bf = get_bound_field(form, "photo")
    attrs = bf.get_widget_attrs(bf.widget, {
        "class": "demo-class"
    })
    assert attrs["class"] == "demo-class"


def test_composer_widget_css_classes():
    # Класс определяется для финального виджета.
    # В данном случае, это виджет, указанный в поле `widgets`.
    form = CustomForm({})
    bf = get_bound_field(form, "gender")
    assert bf.get_widget_attrs(bf.widget)["class"] == "form-check-input"
