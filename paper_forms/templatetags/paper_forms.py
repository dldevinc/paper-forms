from django.template import library

from ..boundfield import BoundField
from ..utils import get_composer

try:
    import jinja2
except ImportError:
    jinja2 = None

register = library.Library()


def _tag(form_field, **attrs):
    form = form_field.form

    bound_field = BoundField(
        form=form_field.form,
        field=form_field.field,
        name=form_field.name,
        composer=get_composer(form),
    )

    # Split `attrs` to widget attributes and context variables
    context = {key[1:]: value for key, value in attrs.items() if key.startswith('_')}
    widget_attrs = {key: value for key, value in attrs.items() if not key.startswith('_')}

    # Special cases: `label` and `help_text` parameters are treated as context variables
    label = widget_attrs.pop("label", None)
    if label is not None:
        context["label"] = label

    help_text = widget_attrs.pop("help_text", None)
    if help_text is not None:
        context["help_text"] = help_text

    # Workaround for attributes with dashes
    widget_attrs = {
        key.replace("__", "-"): value
        for key, value in widget_attrs.items()
    }

    return bound_field.as_widget(attrs=widget_attrs, context=context)


@register.simple_tag
def field(form_field, **attrs):
    return _tag(form_field, **attrs)


if jinja2 is not None:
    from jinja2_simple_tags import StandaloneTag

    class PaperFormExtension(StandaloneTag):
        tags = {"field"}

        def render(self, form_field, **attrs):
            return _tag(form_field, **attrs)

    # django-jinja support
    try:
        from django_jinja import library
    except ImportError:
        pass
    else:
        library.extension(PaperFormExtension)
