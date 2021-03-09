from django.utils.module_loading import import_string

from . import conf


def get_composer(form):
    if hasattr(form, "Composer"):
        return form.Composer()
    else:
        return import_string(conf.DEFAULT_COMPOSER)()
