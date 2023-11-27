# Change Log

## [0.3.0](https://github.com/dldevinc/paper-forms/tree/v0.3.0) - 2023-11-27

### ⚠ BREAKING CHANGES

-   Introducing a new feature to customize form field contexts using the "_" prefix 
    for template tag parameters. Now, parameters prefixed with "_" are treated as template 
    context variables rather than widget attributes. Example:
    ```html
    {% field "name" placeholder="Name" _style="light" %}
    ```
    In this example, `placeholder` signifies a widget attribute, while `style` denotes 
    a template context variable.

### Features

-   Add tests against Python 3.12.

## [0.2.2](https://github.com/dldevinc/paper-forms/tree/v0.2.2) - 2023-10-11

### Features

-   You can now customize form field labels using the `{% field %}` template tag. 
    Set your preferred label values like this: `{% field form.name label="Your name" %}`

## [0.2.1](https://github.com/dldevinc/paper-forms/tree/v0.2.1) - 2023-01-09

### Features

-   Add Python 3.11 support (no code changes were needed, but now we test this release).

## [0.2.0](https://github.com/dldevinc/paper-forms/tree/v0.2.0) - 2022-01-12

-   Support Python 3.10 and Django-4.0
-   Dropped Python 3.6 and 3.7

## [0.1.0](https://github.com/dldevinc/paper-forms/tree/v0.1.0) - 2021-11-24

-   Add support for Django-3.2
-   Drop support for Django-1.11, Django-2.0, Django-2.1, Python-3.5

## [0.0.3](https://github.com/dldevinc/paper-forms/tree/v0.0.3) - 2021-03-16

-   Add `PAPER_FORMS_DEFAULT_FORM_RENDERER` setting

## [0.0.2](https://github.com/dldevinc/paper-forms/tree/v0.0.2) - 2021-03-16

-   Fix missing tempaltes

## [0.0.1](https://github.com/dldevinc/paper-forms/tree/v0.0.1) - 2021-03-15

-   First release
