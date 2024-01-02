from django.forms import CharField, Form, TextInput, Textarea

from paper_forms.boundfield import BoundField
from paper_forms.composer import BaseComposer


def get_boundfield(form: Form, name: str, composer: BaseComposer):
    field = form.fields[name]
    return BoundField(
        form=form,
        field=field,
        name=name,
        composer=composer
    )


class TestWidget:
    def test_default(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
            )

        bf = get_boundfield(MyForm(), "name", BaseComposer())
        assert isinstance(bf.widget, TextInput)

    def test_override(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
            )

        class Composer(BaseComposer):
            widgets = {
                "name": Textarea,
            }

        bf = get_boundfield(MyForm(), "name", Composer())
        assert isinstance(bf.widget, Textarea)


class TestBuildWidgetAttrs:
    def test_default(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
            )

        bf = get_boundfield(MyForm(), "name", BaseComposer())
        attrs = bf.build_widget_attrs(bf.widget)
        assert attrs == {
            "required": True,
            "maxlength": "64"
        }

    def test_override(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
            )

        class Composer(BaseComposer):
            def build_widget_attrs(self, name, attrs, widget):
                attrs = super().build_widget_attrs(name, attrs, widget)
                placeholder = attrs.pop("placeholder", None)
                if placeholder and attrs.get("required"):
                    placeholder += " *"
                if placeholder:
                    attrs["placeholder"] = placeholder
                return attrs

        bf = get_boundfield(MyForm(), "name", Composer())
        attrs = bf.build_widget_attrs(bf.widget, {
            "placeholder": "Your Name",
        })
        assert attrs == {
            "required": True,
            "maxlength": "64",
            "placeholder": "Your Name *",
        }

    def test_override_internal_attributes(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
                widget=TextInput(
                    attrs={
                        "placeholder": "Your Name",
                    }
                )
            )

        class Composer(BaseComposer):
            def build_widget_attrs(self, name, attrs, widget):
                attrs = super().build_widget_attrs(name, attrs, widget)
                placeholder = attrs.pop("placeholder", None)
                if placeholder and attrs.get("required"):
                    placeholder += " *"
                if placeholder:
                    attrs["placeholder"] = placeholder
                return attrs

        bf = get_boundfield(MyForm(), "name", Composer())
        attrs = bf.build_widget_attrs(bf.widget)
        assert attrs == {
            "required": True,
            "maxlength": "64",
            "placeholder": "Your Name *",
        }


class TestGetContext:
    def test_default(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
            )

        bf = get_boundfield(MyForm(), "name", BaseComposer())
        context = bf.get_context(
            bf.widget,
            name="name",
            value="John",
            attrs={"placeholder": "Your Name"},
            extra_context={"theme": "dark"}
        )

        assert context["widget"]["name"] == "name"
        assert context["widget"]["value"] == "John"
        assert context["widget"]["attrs"]["placeholder"] == "Your Name"

        # ignore "widget" data
        context.pop("widget")

        assert context == {
            "label": "Name",
            "help_text": "",
            "css_classes": "",
            "errors": [],
            "theme": "dark",
        }

    def test_form_errors(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
            )

        # Bound form
        form = MyForm({})

        bf = get_boundfield(form, "name", BaseComposer())
        context = bf.get_context(
            bf.widget,
            name="name",
            value="",
        )

        # ignore "widget" data
        context.pop("widget")

        assert context == {
            "label": "Name",
            "help_text": "",
            "css_classes": "",
            "errors": ["This field is required."],
        }

    def test_get_values_from_extra_context(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
                label="This will be overriden",
                help_text="This will be overriden",
            )

        class Composer(BaseComposer):
            labels = {
                "name": "This will be overriden",
            }
            help_texts = {
                "name": "This will be overriden",
            }
            css_classes = {
                "name": "This will be overriden",
            }

        bf = get_boundfield(MyForm(), "name", Composer())
        context = bf.get_context(
            bf.widget,
            name="name",
            value="John",
            extra_context={
                "label": "Your Name",
                "help_text": "Enter your first name",
                "css_classes": "text--red",
            }
        )

        # ignore "widget" data
        context.pop("widget")

        assert context == {
            "label": "Your Name",
            "help_text": "Enter your first name",
            "css_classes": "text--red",
            "errors": [],
        }

    def test_get_values_from_composer(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
                label="This will be overriden",
                help_text="This will be overriden",
            )

        class Composer(BaseComposer):
            labels = {
                "name": "Your Name",
            }
            help_texts = {
                "name": "Enter your first name",
            }
            css_classes = {
                "name": "text--blue",
            }

        bf = get_boundfield(MyForm(), "name", Composer())
        context = bf.get_context(
            bf.widget,
            name="name",
            value="John",
        )

        # ignore "widget" data
        context.pop("widget")

        assert context == {
            "label": "Your Name",
            "help_text": "Enter your first name",
            "css_classes": "text--blue",
            "errors": [],
        }

    def test_get_values_from_field(self):
        class MyForm(Form):
            name = CharField(
                max_length=64,
                label="Your Name",
                help_text="Enter your first name",
            )

        bf = get_boundfield(MyForm(), "name", BaseComposer())
        context = bf.get_context(
            bf.widget,
            name="name",
            value="",
        )

        # ignore "widget" data
        context.pop("widget")

        assert context == {
            "label": "Your Name",
            "help_text": "Enter your first name",
            "css_classes": "",
            "errors": [],
        }


class TestCssClasses:
    def test_get_values_from_composer(self):
        class MyForm(Form):
            error_css_class = "This will be overriden"
            required_css_class = "This will be overriden"

            name = CharField(
                max_length=64,
            )

        class Composer(BaseComposer):
            error_css_class = "invalid"
            required_css_class = "required"

        # Bound form
        form = MyForm({})

        bf = get_boundfield(form, "name", Composer())
        css_classes = bf.css_classes()
        assert css_classes == "invalid required"

    def test_get_values_from_form(self):
        class MyForm(Form):
            error_css_class = "invalid"
            required_css_class = "required"

            name = CharField(
                max_length=64,
            )

        # Bound form
        form = MyForm({})

        bf = get_boundfield(form, "name", BaseComposer())
        css_classes = bf.css_classes()
        assert css_classes == "invalid required"
