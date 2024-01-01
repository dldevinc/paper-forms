import copy
from typing import Any, Optional

from django.forms import BaseForm
from django.forms.renderers import BaseRenderer
from django.forms.widgets import Widget
from django.utils.module_loading import import_string

from .. import conf


class SingletonMeta(type):
    _instances: dict[Any, "BaseComposer"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseComposer(metaclass=SingletonMeta):
    renderer = None
    widgets: dict[str, Any] = None
    labels: dict[str, str] = None
    help_texts: dict[str, str] = None
    css_classes: dict[str, str] = None
    template_names: dict[str, str] = None

    def get_renderer(self, form: BaseForm) -> BaseRenderer:
        renderer = self.renderer or form.default_renderer or conf.DEFAULT_FORM_RENDERER
        if isinstance(renderer, str):
            renderer_class = import_string(renderer)
            return renderer_class()
        elif isinstance(renderer, type):
            return renderer()
        return renderer

    def get_widget(self, name: str) -> Widget:
        if self.widgets and name in self.widgets:
            widget = self.widgets[name]
            if isinstance(widget, type):
                return widget()
            else:
                return copy.deepcopy(widget)

    def get_template_name(self, name: str, widget: Widget) -> str:
        if widget.is_hidden:
            return widget.template_name

        if self.template_names and name in self.template_names:
            return self.template_names[name]

        return self.get_default_template_name(name, widget)

    def get_default_template_name(self, name: str, widget: Widget) -> str:
        return widget.template_name

    def get_label(self, name: str, widget: Widget) -> Optional[str]:
        if self.labels and name in self.labels:
            return self.labels[name]

    def get_help_text(self, name: str, widget: Widget) -> Optional[str]:
        if self.help_texts and name in self.help_texts:
            return self.help_texts[name]

    def get_css_classes(self, name: str, widget: Widget) -> Optional[str]:
        if self.css_classes and name in self.css_classes:
            return self.css_classes[name]

    def build_widget_attrs(self, name: str, attrs: dict, widget: Widget) -> dict:
        # Here you can edit the attributes before they get into the widget
        return attrs or {}

    def build_context(self, name: str, context: dict, widget: Widget) -> dict:
        # Here you can edit the context of the form field
        return context
