# paper-forms

This library provides tools to simplify and customize the form rendering process in Django. 
It includes the `BaseComposer` class for centralized management of form settings and extends 
the functionality of `BoundField` for convenient customization of form fields.

[![PyPI](https://img.shields.io/pypi/v/paper-forms.svg)](https://pypi.org/project/paper-forms/)
[![Build Status](https://github.com/dldevinc/paper-forms/actions/workflows/tests.yml/badge.svg)](https://github.com/dldevinc/paper-forms)
[![Software license](https://img.shields.io/pypi/l/paper-forms.svg)](https://pypi.org/project/paper-forms/)

### Compatibility

-   `python` >= 3.9
-   `django` >= 3.2

### Features

-   [Jinja2](https://jinja.palletsprojects.com/) support.
-   [django-jinja](https://github.com/niwinz/django-jinja) support.

## Table of Contents

1. [Installation](#Installation)
2. [Basic Usage](#Basic-Usage)
3. [Composer Configuration](#Composer-Configuration)
   1. [Specifying Custom Template Names](#Specifying-Custom-Template-Names)
   2. [Customizing Form Field Rendering in Composer](#Customizing-Form-Field-Rendering-in-Composer)
   3. [Customizing Composer Class](#Customizing-Composer-Class)
4. [Template Tags](#Template-Tags)
5. [Common Issues and Workarounds](#Common-Issues-and-Workarounds)

## Installation

To get started with `paper-forms`, you need to install the library using `pip`. 
Ensure you have Python 3.9 or later installed in your environment.

```shell
pip install paper-forms
```

Next, add "paper_forms" to the `INSTALLED_APPS` in your Django project's `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "paper_forms",
)
```

## Basic Usage

Start by creating a simple Django form. No mixins or third-party classes are required. 
Just define your form as you normally would using Django's `forms` module.

```python
# forms.py
from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
```

Now, let's render the form in your template using the `{% field %}` template tag 
provided by `paper-forms`. This tag allows you to render form fields with enhanced 
customization.

```html
<!-- example_template.html -->
{% load paper_forms %}

<form method="post">
  {% field form.name %}
  {% field form.age %}
</form>
```

The rendered HTML will be similar to the standard Django form rendering, but with 
the added flexibility provided by `paper-forms`. This sets the foundation for integrating 
`paper-forms` seamlessly into your Django project.

## Composer Configuration

The real power of `paper-forms` lies in the ability to customize form rendering 
using the `BaseComposer` class. Let's explore how you can leverage this class to tailor 
the rendering of your forms.

One of the key features of `paper-forms` is the ability to customize form widgets. 
In your Django form, you can define a `Composer` class that inherits from `BaseComposer` 
to specify different widgets for specific fields.

```python
# forms.py
from django import forms
from paper_forms.composer import BaseComposer

class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField()

    class Composer(BaseComposer):
        widgets = {
            "password": forms.PasswordInput,
        }
```

In this example, the `Composer` class defines a custom widget for the "password" field. 
This allows you to have fine-grained control over the rendering of individual form fields.

`paper-forms` also allows you to set labels and help text for form fields, either 
globally or on a per-field basis.

```python
# forms.py
from django import forms
from paper_forms.composer import BaseComposer

class ExampleForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()

    class Composer(BaseComposer):
        labels = {
            "name": "Your Full Name",
            "age": "Your Age",
        }
        help_texts = {
            "name": "Enter your full name as it appears on official documents.",
            "age": "Please provide your current age.",
        }
```

Here, the `Composer` class provides labels and help text for the "name" and "age" fields, 
offering clear instructions to users interacting with your forms.

Additionally, developers can enhance the customization of the form's appearance 
by utilizing the `error_css_class` and `required_css_class` attributes 
within the `Composer` class. These attributes allow you to define specific CSS classes 
for handling errors and indicating required fields, respectively. Notably, any values 
set for these attributes in the `Composer` class take precedence over those specified 
at the form level.

### Specifying Custom Template Names

When using `paper-forms`, you have the flexibility to create custom templates for 
individual form fields. This can be achieved by leveraging the `Composer` class 
and specifying custom template names for each field. Let's go through an example 
of how a custom form field template might look:

Assume you have a Django form with a field named "name," and you want to create 
a custom template for rendering this specific field.

1.  **Create the Custom Template**<br>
    Create a new HTML file, let's call it `custom_field.html`, and place 
    it in your Django app's templates directory. Here's a simplified example of how 
    the template might look:
    ```html
    <!-- custom_field.html -->

    <div class="form-field {{ css_classes }}">
        <label for="{{ widget.attrs.id }}">{{ label }}</label>
 
        <!-- include default widget template -->
        {% include widget.template_name %}

        <!-- show field errors -->
        {% if errors %}
        <ul>
            {% for error in errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
        {% endif %}

        <!-- show help text -->
        {% if help_text %}
        <small>{{ help_text }}</small>
        {% endif %}
    </div>
    ```
    In this example, the template includes a custom structure for rendering 
    the form field, including a label, the actual form widget, error messages, 
    and help text.
2.  **Update the Composer Class**<br>
    Now, update the `Composer` class in your Django form to specify the custom 
    template name for the "name" field:
    ```python
    from django import forms
    from paper_forms.composer import BaseComposer

    class ExampleForm(forms.Form):
        name = forms.CharField()
        age = forms.IntegerField()

        class Composer(BaseComposer):
            template_names = {
                "name": "path/to/custom_field.html",
            }
    ```
    Ensure that the path provided in template_names matches the location of your custom 
    template file.
3.  **Render the Form in Your Template**<br>
    In your Django template where you render the form, use the `{% field %}` template 
    tag for the "name" field:
    ```html
    {% load paper_forms %}

    <form method="post">
        {% field form.name %}
        {% field form.age %}
        <button type="submit">Submit</button>
    </form>
    ```
    When the form is rendered, the "name" field will use your custom template, 
    while other fields will follow the default rendering.

By following these steps, you can create and apply custom templates for specific form 
fields, providing a tailored look and feel for different parts of your Django forms.

### Customizing Form Field Rendering in Composer

The `paper-forms` library provides extensive flexibility through the `Composer` class, 
allowing you to customize the rendering of form fields. In addition to specifying custom 
templates, you can achieve advanced customization by overriding methods in the 
`BaseComposer` class. Let's explore an example of how to override methods to replace 
`labels` with `placeholders` across all form fields.

Suppose you want to make a global change to the rendering of form fields, replacing 
labels with placeholders.

Step 1: Create a Custom Composer.

Create a custom `Composer` subclass with the desired customization for form 
field rendering.

```python
# composers.py
from paper_forms.composer import BaseComposer

class CustomComposer(BaseComposer):
    placeholders: dict = None

    def get_label(self, name, widget):
        # Override get_label method to return an empty string 
        # for all fields.
        return ""

    def build_widget_attrs(self, name, attrs, widget):
        attrs = super().build_widget_attrs(name, attrs, widget)
        placeholder = attrs.get("placeholder")
        if placeholder is None and self.placeholders:
            placeholder = self.placeholders[name]
        if placeholder:
            attrs["placeholder"] = placeholder
        return attrs
```

Step 2: Use Custom Composer in a Django Form.

Apply the custom `CustomComposer` class to a Django form.

```python
# forms.py
from django import forms
from .composers import CustomComposer


class ExampleForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()

    class Composer(CustomComposer):
        placeholders = {
            "name": "Enter your name",
            "age": "Enter your age",
        }
```

Step 3: Render the Form in Your Template.

Use the `{% field %}` template tag to render the form in your template.

```html
{% load paper_forms %}

<form method="post">
    {% field form.name %}
    {% field form.age %}
    <button type="submit">Submit</button>
</form>
```

With this setup, the "name" and "age" fields will have placeholders instead of labels.

### Customizing Composer Class

In addition to the specific methods discussed earlier, the `BaseComposer` class 
in the `paper-forms` library provides several other methods that developers can override 
to further customize form field rendering. Below are some of the additional methods 
available for customization:

`get_widget(self, name: str) -> Widget`

Retrieves a widget for a specific form field. By default, it looks up the widget 
in the `widgets` dictionary. If `None` is returned, the default widget for the field 
will be used.

`get_template_name(self, name: str, widget: Widget) -> str`

Determines the template name to be used for rendering a form field. It considers 
hidden widgets, specific template names in the template_names dictionary, and 
falls back to the default template name.

`get_default_template_name(self, name: str, widget: Widget) -> str`

This method plays a crucial role in simplifying the creation of Composer classes for 
frameworks like Bootstrap. This method is designed to facilitate the customization 
of form field templates without affecting the ability to specify template paths via 
the `template_names` attribute in the `Composer` class.

When rendering a form field, the `get_default_template_name` method is called 
to determine the default template name based on the provided field name and widget. 
This method can be overridden in custom Composer classes to set a default template name, 
allowing for a more streamlined implementation of framework-specific Composers.

```python
from django.forms.widgets import TextInput, NumberInput
from paper_forms.composer import BaseComposer

class FrameworkComposer(BaseComposer):
    def get_default_template_name(self, name, widget) -> str:
        if isinstance(widget, TextInput):
            return f"bootstrap/text_field.html"
        elif isinstance(widget, NumberInput):
            return f"bootstrap/number_field.html"

        # Fall back to the default behavior
        return super().get_default_template_name(name, widget)
```

`get_label(self, name: str, widget: Widget) -> Optional[str]`

Retrieves the label for a form field. It looks up the label in the `labels` dictionary.
If `None` is returned, the default label for the field will be used.

`get_help_text(self, name: str, widget: Widget) -> Optional[str]`

Retrieves the help text for a form field. It looks up the help text in the `help_texts` 
dictionary. If `None` is returned, the default help text for the field will be used.

`get_css_classes(self, name: str, widget: Widget) -> Optional[str]`

Retrieves the CSS classes for a form field. It looks up the CSS classes 
in the `css_classes` dictionary.

`build_widget_attrs(self, name: str, attrs: Optional[dict], widget: Widget) -> dict`

Builds and customizes the attributes for a form field's widget. Developers can add, 
remove, or modify attributes based on field names or other criteria.

`build_context(self, name: str, context: Optional[dict], widget: Widget) -> dict`

Builds the context to be passed to the form field template. Developers can add 
or modify context variables based on field names or other conditions.

## Template Tags

`paper-forms` provides template tags to simplify the integration of the library into 
your Django templates. The primary tag is `{% field %}`, which allows you to render 
form fields with enhanced customization options.

The `{% field %}` tag is the key to leveraging the features provided by `paper-forms`. 
It allows you to render form fields with various attributes and context variables.

```html
{% load paper_forms %}

<form method="post">
  {% field form.name placeholder="Enter your name" %}
  {% field form.age placeholder="Enter your age" _style="light" %}
</form>
```

In this example, the `{% field %}` tag is used to render the "name" and "age" fields 
of the form. Attributes such as `placeholder` and `style` are passed as parameters 
to customize the rendering.

The `{% field %}` tag supports adding variables to the form field template using 
the "_" prefix in the template tag parameters. These variables become part 
of the template context for the form field.

In the example above, the `placeholder` attribute is a widget attribute, while 
the `_style` is a template context variable. Parameters with a leading underscore, 
such as `_style`, are treated as template context variables.

## Configuration

`paper-forms` provides additional configuration options that you can set in your 
Django project's settings.

You can specify the default `Composer` class to be used for any form that doesn't specify 
a particular composer. This is set using the `PAPER_FORMS_DEFAULT_COMPOSER` setting.

```python
# settings.py

PAPER_FORMS_DEFAULT_COMPOSER = "myapp.composers.CustomComposer"
```

Here, `myapp.composers.CustomComposer` is the custom composer class you want to use 
as the default.

The default form renderer can be set using the `PAPER_FORMS_DEFAULT_FORM_RENDERER` setting.

```python
# settings.py

PAPER_FORMS_DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
```

In this example, `django.forms.renderers.TemplatesSetting` is used as the default 
form renderer.

## Common Issues and Workarounds

In the course of using `paper-forms`, you may encounter some common issues. This section 
provides explanations and workarounds for these issues to help you navigate potential 
challenges.

### Dashes in Attribute Names

If you are trying to specify an attribute with dashes in the `{% field %}` template tag, 
like `data-src`, you might face limitations. This is due to the restrictive nature of 
`@simple_tag`, which [does not allow dashes]((https://code.djangoproject.com/ticket/21077))
in kwargs names.

To overcome this limitation, use double underscores. All double underscores in 
`{% field %}` arguments are replaced with single dashes. For example:

```html
{% field form.name data__original__name="Name" %}
```

This would render to something like

```html
<input ... data-original-name="Name" />
```

### `FORM_RENDERER` Setting with Third-Party Template Engines

If you are using `django-jinja` or any other third-party template engine as your default
template engine, and you want to use it for your form field templates, you might face 
challenges. Django's form widgets are rendered using form renderers, and changing the 
`FORM_RENDERER` setting can break the admin interface.

Follow these steps to work around this problem:

1.  Make built-in widget templates searchable:
    ```python
    # settings.py

    from pathlib import Path
    from django import forms

    TEMPLATES = [
        {
            "NAME": "jinja2",
            "BACKEND": "django_jinja.backend.Jinja2",
            "DIRS": [
                BASE_DIR / "templates",
                Path(forms.__file__).parent / "jinja2"
            ],
            # ...
        }
    ]
    ```

2.  Use `TemplateSetting` renderer for your forms or implement your own. You can achieve 
    this in several ways:
    * Set the `PAPER_FORMS_DEFAULT_FORM_RENDERER` setting in `settings.py`:
      ```python
      # settings.py

      PAPER_FORMS_DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
      ```
    * Specify the `default_renderer` attribute in your form:
      ```python
      from django import forms
      from django.forms.renderers import TemplatesSetting

      class ExampleForm(forms.Form):
          default_renderer = TemplatesSetting
          # ...
      ```
    * Set the `renderer` field in your `Composer` class:
      ```python
      from django import forms
      from paper_forms.composer import BaseComposer

      class ExampleForm(forms.Form):
          name = forms.CharField()

          class Composer(BaseComposer):
              renderer = "django.forms.renderers.TemplatesSetting"
      ```
