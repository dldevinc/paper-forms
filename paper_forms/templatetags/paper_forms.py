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

    # support "data-*" attributes
    attrs = {
        key.replace("__", "-"): value
        for key, value in attrs.items()
    }

    return bound_field.as_widget(attrs=attrs)


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
