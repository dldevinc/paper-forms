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
    # other apps
    "paper_forms",
)
```

## Features
* [Jinja2](https://jinja.palletsprojects.com/) support.
* [django-jinja](https://github.com/niwinz/django-jinja) support.
* Add or replace attributes to form fields using a template tag.

## Usage

Let’s create our first Django paper form.

```python
from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
```

Yeap. No mixins, no base classes. Just a simple Django form.

Now, let’s render our form:
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
exactly like `{{ form.field }}`.

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
All double-underscore in `{% field %}` arguments are replaced with single dash:

```html
{% field form.name data__original__name="Name"  %}
<!-- would render to something like --> 
<input ... data-original-name="Name" />
```

### Write your own field templates

Example: 
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

The `paper_forms` not only makes it possible to override widget templates,
but also *extends* them to form field templates.

### Override widget template with `Composer`

Composer is a tool which gives you full control over form field rendering.

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
of the `ModelForm`'s `Meta` class.

**The data specified in the composer fields have the highest priority.**

### Create your own `Composer` subclass for web frameworks

Example:
```python
from django.forms import widgets
from paper_forms.composers.base import BaseComposer


class Bootstrap4(BaseComposer):
    def get_default_template_name(self, widget):
        # Overrides the widget template, but has a lower priority 
        # than the 'template_names' field.
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
