from django.forms import Form, HiddenInput, NumberInput, TextInput
from django.forms.renderers import Jinja2, TemplatesSetting

from paper_forms.composer import BaseComposer


class TestSingleton:
    def test_base(self):
        composer1 = BaseComposer()
        composer2 = BaseComposer()
        assert composer1 is composer2

    def test_subclass(self):
        class Composer(BaseComposer):
            pass

        composer1 = BaseComposer()
        composer2 = Composer()
        composer3 = Composer()
        assert composer1 is not composer2
        assert composer2 is composer3


class TestGetRenderer:
    def test_string(self):
        class Composer(BaseComposer):
            renderer = "django.forms.renderers.Jinja2"

        composer = Composer()
        renderer = composer.get_renderer(Form())
        assert isinstance(renderer, Jinja2)

    def test_instance(self):
        class Composer(BaseComposer):
            renderer = Jinja2()

        composer = Composer()
        renderer = composer.get_renderer(Form())
        assert isinstance(renderer, Jinja2)

    def test_form_renderer(self, paper_conf):
        class MyForm(Form):
            default_renderer = Jinja2

        composer = BaseComposer()
        renderer = composer.get_renderer(MyForm())
        assert isinstance(renderer, Jinja2)

    def test_default(self, paper_conf):
        paper_conf.DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

        composer = BaseComposer()
        renderer = composer.get_renderer(Form())
        assert isinstance(renderer, TemplatesSetting)

    def test_empty(self):
        composer = BaseComposer()
        renderer = composer.get_renderer(Form())
        assert renderer is None


class TestGetWidget:
    def test_empty(self):
        composer = BaseComposer()
        widget = composer.get_widget("name")
        assert widget is None

    def test_override_class(self):
        class Composer(BaseComposer):
            widgets = {
                "name": TextInput,
            }

        composer = Composer()
        widget = composer.get_widget("name")
        assert isinstance(widget, TextInput)

    def test_override_instance(self):
        class Composer(BaseComposer):
            widgets = {
                "name": TextInput(),
            }

        composer = Composer()
        widget = composer.get_widget("name")
        assert isinstance(widget, TextInput)

    def test_missing_name(self):
        class Composer(BaseComposer):
            widgets = {
                "name": TextInput(),
            }

        composer = Composer()
        widget = composer.get_widget("password")
        assert widget is None


class TestGetTemplateName:
    def test_default(self):
        composer = BaseComposer()
        template_name = composer.get_template_name("name", widget=NumberInput())
        assert template_name == "django/forms/widgets/number.html"

    def test_override(self):
        class Composer(BaseComposer):
            template_names = {
                "name": "path/to/widget.html",
            }

        composer = Composer()
        template_name = composer.get_template_name("name", widget=NumberInput())
        assert template_name == "path/to/widget.html"

    def test_hidden_widget_priority(self):
        class Composer(BaseComposer):
            template_names = {
                "name": "path/to/widget.html",
            }

        composer = Composer()
        template_name = composer.get_template_name("name", widget=HiddenInput())
        assert template_name == "django/forms/widgets/hidden.html"

    def test_missing_name(self):
        class Composer(BaseComposer):
            template_names = {
                "name": "path/to/widget.html",
            }

        composer = Composer()
        template_name = composer.get_template_name("about", widget=TextInput())
        assert template_name == "django/forms/widgets/text.html"


class TestGetLabel:
    def test_empty(self):
        composer = BaseComposer()
        label = composer.get_label("name", widget=TextInput())
        assert label is None

    def test_override(self):
        class Composer(BaseComposer):
            labels = {
                "name": "Your Name",
            }

        composer = Composer()
        label = composer.get_label("name", widget=TextInput())
        assert label == "Your Name"

    def test_missing_name(self):
        class Composer(BaseComposer):
            labels = {
                "name": "Your Name",
            }

        composer = Composer()
        label = composer.get_label("age", widget=NumberInput())
        assert label is None


class TestGetHelpText:
    def test_empty(self):
        composer = BaseComposer()
        help_text = composer.get_help_text("name", widget=TextInput())
        assert help_text is None

    def test_override(self):
        class Composer(BaseComposer):
            help_texts = {
                "name": "Enter your first name",
            }

        composer = Composer()
        help_text = composer.get_help_text("name", widget=TextInput())
        assert help_text == "Enter your first name"

    def test_missing_name(self):
        class Composer(BaseComposer):
            help_texts = {
                "name": "Enter your first name",
            }

        composer = Composer()
        help_text = composer.get_help_text("age", widget=NumberInput())
        assert help_text is None


class TestGetCssClasses:
    def test_empty(self):
        composer = BaseComposer()
        css_classes = composer.get_css_classes("name", widget=TextInput())
        assert css_classes is None

    def test_override(self):
        class Composer(BaseComposer):
            css_classes = {
                "name": "red blue green",
            }

        composer = Composer()
        css_classes = composer.get_css_classes("name", widget=TextInput())
        assert css_classes == "red blue green"

    def test_missing_name(self):
        class Composer(BaseComposer):
            css_classes = {
                "name": "red blue green",
            }

        composer = Composer()
        css_classes = composer.get_css_classes("age", widget=NumberInput())
        assert css_classes is None


class TestBuildWidgetAttrs:
    def test_empty(self):
        composer = BaseComposer()
        widget_attrs = composer.build_widget_attrs("name", None, widget=TextInput())
        assert widget_attrs == {}

    def test_attrs(self):
        composer = BaseComposer()
        widget_attrs = composer.build_widget_attrs("name", {
            "placeholder": "Name",
        }, widget=TextInput())
        assert widget_attrs == {
            "placeholder": "Name",
        }


class TestBuildContext:
    def test_empty(self):
        composer = BaseComposer()
        context = composer.build_context("name", None, widget=TextInput())
        assert context == {}

    def test_attrs(self):
        composer = BaseComposer()
        base_context = {
            "theme": "dark",
        }
        context = composer.build_widget_attrs("name", base_context, widget=TextInput())
        assert context is base_context
