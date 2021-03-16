from django.conf import settings

DEFAULT_COMPOSER = getattr(settings, "PAPER_FORMS_DEFAULT_COMPOSER", "paper_forms.composers.base.BaseComposer")
DEFAULT_FORM_RENDERER = getattr(settings, "PAPER_FORMS_DEFAULT_FORM_RENDERER", None)
