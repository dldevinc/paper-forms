from typing import Any, Dict

from django.utils.module_loading import import_string


class SingletonMeta(type):
    _instances = {}  # type: Dict[Any, 'BaseComposer']

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseComposer(metaclass=SingletonMeta):
    renderer = None
    widgets = None  # type: Dict[str, Any]
    labels = None   # type: Dict[str, Any]
    help_texts = None   # type: Dict[str, Any]
    template_names = None   # type: Dict[str, Any]

    def get_renderer(self, form):
        if isinstance(self.renderer, str):
            renderer_class = import_string(self.renderer)
            return renderer_class()

        return self.renderer or form.renderer

    def get_default_template_name(self, widget):
        """
        Overrides the widget template, but has a lower priority
        than the 'template_names' field.
        """
        return widget.template_name

    def get_default_css_classes(self, widget):
        """
        Adds default CSS classes that can be overridden
        in the {% field %} template tag.
        """
        return ""

    def build_widget_attrs(self, widget, attrs):
        # Here you can edit the attributes before they get into the widget
        return attrs

    def build_widget_context(self, widget, context):
        # Here you can edit the context of the widget
        return context
