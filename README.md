# paper-forms
A form templating app for Django

[![PyPI](https://img.shields.io/pypi/v/paper-forms.svg)](https://pypi.org/project/paper-forms/)
[![Build Status](https://travis-ci.com/dldevinc/paper-forms.svg?branch=master)](https://travis-ci.org/dldevinc/paper-forms)
[![Software license](https://img.shields.io/pypi/l/paper-forms.svg)](https://pypi.org/project/paper-forms/)

## Compatibility
* `python` >= 3.5
* `django` >= 1.11

## Installation
Install the latest release with pip:

```shell
pip install paper-forms
```

Add `paper_forms` to your INSTALLED_APPS in `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "paper_forms",
)
```

## Features
* [Jinja2](https://jinja.palletsprojects.com/) support.
* [django-jinja](https://github.com/niwinz/django-jinja) support.
* Add or replace attributes to form fields using a template tag.

## Usage

Let’s create our first Django form.

```python
from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
```
No mixins. No third-party classes. Just a simple Django form.

Now, let’s render our form by using the `{% field %}` template tag:
```html
{% load paper_forms %}

<form method="post">
  {% field form.name %}
  {% field form.age %}
</form>
```

This is exactly the html that you would get:

```html
<form method="post">
  <input type="text" name="name" id="id_name" required />
  <input type="number" name="age" id="id_age" required />
</form>
```

As you can see, a `{% field form.field %}` template tag behaves 
exactly like `{{ form.field }}`. This is how you can integrate
`paper-forms` with your Django project.

Now, let's add some customization.

## Customization

The simplest thing you can do is to add (or replace) attributes to the widget:
```html
{% load paper_forms %}

<form method="post">
  {% field form.name placeholder="Enter your name" %}
  {% field form.age placeholder="Enter your age" title=form.age.label %}
</form>
```

Result:
```html
<form method="post">
  <input type="text" name="name" id="id_name" placeholder="Enter your name" required />
  <input type="number" name="age" title="Age" required placeholder="Enter your age" id="id_age" />
</form>
```

**Note** that you cannot specify an attribute with a dashes, like `data-src`.
This is because `@simple_tag` is quite restrictive and [doesn't allow dashes](https://code.djangoproject.com/ticket/21077) 
in kwargs names. 

A way to get around this limitation is to use double-underscore.
All double-underscores in `{% field %}` arguments are replaced with single dashes:

```html
{% field form.name data__original__name="Name"  %}
```

would render to something like

```html
<input ... data-original-name="Name" />
```

### Override widget templates with `Composer`

Composer is a tool which gives you full control over form 
field rendering.

Example:

```python
from django import forms
from paper_forms.composers.base import BaseComposer


class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField()

    class Composer(BaseComposer):
        widgets = {
            "password": forms.PasswordInput
        }
        template_names = {
            "password": "path/to/field_template.html"
        }
        labels = {
            "password": "Enter your password"
        }
        help_texts = {
            "password": "Your password must be 8-20 characters long, " 
                        "contain letters and numbers, and must not contain " 
                        "spaces, special characters, or emoji."
        }
```

As you can see, attributes such as `widgets`, `labels` and `help_texts`
are very similar to [those](https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#overriding-the-default-fields)
of the `ModelForm`'s `Meta` class. **The data specified in the Composer 
fields have the highest priority.**

There is also the `template_names` attribute which allows you to
override a form field templates. Form field template context *is a 
widget context*, extended with `label`, `errors` and `help_text` 
values. You can add your own data by overriding the
`build_widget_context` method in your Composer class.

Template example:
```html
<div class="form-field">
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

### Create your own `Composer` subclass for web frameworks

Example:
```python
from django.forms import widgets
from paper_forms.composers.base import BaseComposer


class Bootstrap4(BaseComposer):
    def get_default_template_name(self, widget):
        # Overrides the widget template, but has a lower priority
        # than the 'template_names' attribute of the Composer class.
        if isinstance(widget, widgets.CheckboxInput):
            return "paper_forms/bootstrap4/checkbox.html"
        else:
            return "paper_forms/bootstrap4/input.html"

    def get_default_css_classes(self, widget):
        # Adds default CSS classes that can be overridden 
        # in the {% field %} template tag.
        if isinstance(widget, widgets.CheckboxInput):
            return "form-check-input"
        else:
            return "form-control"
```

## Settings

* `PAPER_FORMS_DEFAULT_COMPOSER`<br>
  Default Composer class to be used for any Form that don’t specify 
  a particular composer.<br>
  Default: `paper_forms.composers.base.BaseComposer`

* `PAPER_FORMS_DEFAULT_FORM_RENDERER`<br>
  The class that renders form widgets.<br>
  Default: `None`

## A `FORM_RENDERER` problem

If you use `django-jinja` (or any other third-party template engine) as your default 
template engine, you may also want to use it for your form field templates. 
It's a bit tricky because Django's form widgets are rendered using [form renderers](https://docs.djangoproject.com/en/3.1/ref/forms/renderers/#built-in-template-form-renderers).

It means that even if your page are rendered with `django-jinja`, the form on
that page renders through Django Templates. 

You should not change [FORM_RENDERER](https://docs.djangoproject.com/en/3.1/ref/settings/#form-renderer) 
setting, because it can break the admin interface. Most of the third-party
widgets are designed for the Django Templates.

Two steps are needed to get around this problem.

1. Make built-in widget templates searcheable.
   
    ```python
    # settings.py
   
    from django.forms.renderers import ROOT  # <---
    
    TEMPLATES = [
        {
            "NAME": "jinja2",
            "BACKEND": "django_jinja.backend.Jinja2",
            "DIRS": [
                BASE_DIR / "templates",
                ROOT / "jinja2"              # <---
            ],
            # ...
        }
   ]
    ```

2. Use `TemplateSettings` renderer for you forms, or implement your own.
   There are several ways to do this:
   1. `PAPER_FORMS_DEFAULT_FORM_RENDERER` setting.
      ```python
      # settings.py
      
      PAPER_FORMS_DEFAULT_FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
      ```
   2. [Form.default_renderer](https://docs.djangoproject.com/en/3.1/ref/forms/api/#django.forms.Form.default_renderer)
      ```python
      from django import forms
      from django.forms.renderers import TemplatesSetting

      class ExampleForm(forms.Form):
          default_renderer = TemplatesSetting
          # ...
      ```
   3. `Composer.renderer` field
      ```python
      from django import forms
      from paper_forms.composers.base import BaseComposer
      
      
      class ExampleForm(forms.Form):
          name = forms.CharField()
      
          class Composer(BaseComposer):
              renderer = "django.forms.renderers.TemplatesSetting"
      ```
      