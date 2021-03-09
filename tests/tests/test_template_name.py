from django import forms

from paper_forms.composers.bootstrap4 import Bootstrap4

from .utils import get_bound_field


class SimpleForm(forms.Form):
    name = forms.CharField()
    honeypot = forms.CharField(
        widget=forms.HiddenInput
    )


class BootstrapForm(forms.Form):
    honeypot = forms.CharField(
        widget=forms.HiddenInput
    )
    name = forms.CharField()
    over_18 = forms.BooleanField()
    gender = forms.ChoiceField(
        choices=(
            ("m", "Male"),
            ("f", "Female"),
        ),
        widget=forms.RadioSelect
    )
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
    honeypot = forms.CharField(
        widget=forms.HiddenInput
    )
    name = forms.CharField()
    password = forms.CharField()

    class Composer(Bootstrap4):
        widgets = {
            "password": forms.PasswordInput,
        }
        template_names = {
            "honeypot": "path/to/hidden.html",
            "name": "path/to/widget.html",
            "password": "path/to/password.html",
        }


def test_default_template_name():
    # Шаблон по умолчанию
    simple_bf = get_bound_field(SimpleForm(), "name")
    assert simple_bf.get_template_name(simple_bf.widget) == "django/forms/widgets/text.html"


def test_default_composer_template_name():
    # Шаблоны, переопределенные в методе `get_default_template_name` composer'a
    form = BootstrapForm()

    input_bf = get_bound_field(form, "name")
    assert input_bf.get_template_name(input_bf.widget) == "paper_forms/bootstrap4/input.html"

    checkbox_bf = get_bound_field(form, "over_18")
    assert checkbox_bf.get_template_name(checkbox_bf.widget) == "paper_forms/bootstrap4/checkbox.html"

    select_bf = get_bound_field(form, "gender")
    assert select_bf.get_template_name(select_bf.widget) == "paper_forms/bootstrap4/radio_select.html"

    checkbox_select_bf = get_bound_field(form, "day")
    assert checkbox_select_bf.get_template_name(checkbox_select_bf.widget) == "paper_forms/bootstrap4/checkbox_select.html"

    file_bf = get_bound_field(form, "photo")
    assert file_bf.get_template_name(file_bf.widget) == "paper_forms/bootstrap4/file.html"


def test_composer_template_names():
    # Шаблон, переопределенный в поле `template_names`, имеет наивысший приоритет
    form = CustomForm()
    bf = get_bound_field(form, "name")
    assert bf.get_template_name(bf.widget) == "path/to/widget.html"

    # ... даже для переопределенного виджета
    paasword_bf = get_bound_field(form, "password")
    assert paasword_bf.get_template_name(paasword_bf.widget) == "path/to/password.html"


def test_hidden_widget_template_name():
    # Скрытые виджеты всегда рендерятся своим стандартным шаблоном
    simple_bf = get_bound_field(SimpleForm(), "honeypot")
    assert simple_bf.get_template_name(simple_bf.widget) == "django/forms/widgets/hidden.html"

    bootstrap_bf = get_bound_field(BootstrapForm(), "honeypot")
    assert bootstrap_bf.get_template_name(bootstrap_bf.widget) == "django/forms/widgets/hidden.html"

    custom_bf = get_bound_field(CustomForm(), "honeypot")
    assert custom_bf.get_template_name(custom_bf.widget) == "django/forms/widgets/hidden.html"
