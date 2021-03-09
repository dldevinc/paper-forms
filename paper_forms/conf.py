from django.conf import settings

DEFAULT_COMPOSER = getattr(settings, "PAPER_FORMS_DEFAULT_COMPOSER", "paper_forms.composers.base.BaseComposer")
WIDGET_ATTR_PREFIX = getattr(settings, "PAPER_FORMS_WIDGET_ATTR_PREFIX", "widget__")
