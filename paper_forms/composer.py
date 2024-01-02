import copy
from typing import Any, Optional, ClassVar

from django.forms import BaseForm
from django.forms.renderers import BaseRenderer
from django.forms.widgets import Widget
from django.utils.module_loading import import_string

from . import conf

__all__ = ["BaseComposer"]


class SingletonMeta(type):
    _instances: dict[Any, "BaseComposer"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseComposer(metaclass=SingletonMeta):
    renderer = None
    error_css_class: ClassVar[str] = None
    required_css_class: ClassVar[str] = None
    widgets: ClassVar[dict[str, Any]] = None
    labels: ClassVar[dict[str, str]] = None
    help_texts: ClassVar[dict[str, str]] = None
    css_classes: ClassVar[dict[str, str]] = None
    template_names: ClassVar[dict[str, str]] = None

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
        # A hidden widgets should have a higher priority.
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

    def build_widget_attrs(self, name: str, attrs: Optional[dict], widget: Widget) -> dict:
        return attrs or {}

    def build_context(self, name: str, context: Optional[dict], widget: Widget) -> dict:
        return context or {}
