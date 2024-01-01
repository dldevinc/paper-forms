import datetime
from typing import Any

import django
from django.forms.boundfield import BoundField as _BoundField
from django.forms.boundfield import BoundWidget
from django.forms.widgets import Widget
from django.utils.functional import cached_property

from .composers.base import BaseComposer


class BoundField(_BoundField):
    def __init__(self, form, field, name, composer):
        super().__init__(form, field, name)
        self.composer = composer    # type: BaseComposer

    def as_widget(
        self,
        widget: Widget = None,
        attrs: dict = None,
        only_initial: bool = False,
        extra_context: dict = None
    ):
        widget = widget or self.widget
        if self.field.localize:
            widget.is_localized = True

        attrs = attrs or {}
        attrs = self.build_widget_attrs(widget, attrs)
        if self.auto_id and "id" not in widget.attrs:
            attrs.setdefault("id", self.html_initial_id if only_initial else self.auto_id)

        if django.VERSION >= (4, 2) and only_initial and self.html_initial_name in self.form.data:
            # Propagate the hidden initial value.
            value = self.form._widget_data_value(
                self.field.hidden_widget(),
                self.html_initial_name,
            )
        else:
            value = self.value()

        context = self.get_context(
            widget,
            name=self.html_initial_name if only_initial else self.html_name,
            value=value,
            attrs=attrs,
            extra_context=extra_context,
        )

        return widget._render(
            template_name=self.composer.get_template_name(self.name, widget),
            context=self.composer.build_context(self.name, context, widget),
            renderer=self.composer.get_renderer(self.form),
        )

    def build_widget_attrs(self, widget: Widget, attrs: dict = None) -> dict:
        attrs = attrs or {}
        attrs = super().build_widget_attrs(attrs, widget)
        return self.composer.build_widget_attrs(self.name, attrs, widget)

    def get_context(
        self,
        widget: Widget,
        name: str,
        value: Any,
        attrs: dict = None,
        extra_context: dict = None
    ) -> dict:
        widget_context = widget.get_context(
            name=name,
            value=value,
            attrs=attrs
        )
        extra_context = extra_context or {}
        context = dict(widget_context, **extra_context)

        if "label" not in context:
            label = self.composer.get_label(self.name, widget)
            if label is None:
                label = self.label
            context["label"] = label

        if "help_text" not in context:
            help_text = self.composer.get_help_text(self.name, widget)
            if help_text is None:
                help_text = self.help_text
            context["help_text"] = help_text

        if "css_classes" not in context:
            extra_css_classes = self.composer.get_css_classes(self.name, widget)
            context["css_classes"] = self.css_classes(extra_css_classes)

        context["errors"] = self.errors

        return context

    @cached_property
    def widget(self) -> Widget:
        widget = self.composer.get_widget(self.name)
        if widget is None:
            widget = self.field.widget

        return widget

    @cached_property
    def subwidgets(self) -> list[BoundWidget]:
        # Use self.widget instead of self.field.widget
        id_ = self.widget.attrs.get("id") or self.auto_id
        attrs = {"id": id_} if id_ else {}
        attrs = self.build_widget_attrs(attrs)
        return [
            BoundWidget(self.widget, widget, self.form.renderer)
            for widget in self.widget.subwidgets(
                self.html_name, self.value(), attrs=attrs
            )
        ]

    @property
    def data(self) -> Any:
        # Use self.widget instead of self.field.widget
        if django.VERSION >= (4, 0):
            return self.form._widget_data_value(self.widget, self.html_name)
        else:
            return self.widget.value_from_datadict(
                self.form.data, self.form.files, self.html_name
            )

    @property
    def is_hidden(self) -> bool:
        # Use self.widget instead of self.field.widget
        return self.widget.is_hidden

    @property
    def id_for_label(self) -> str:
        # Use self.widget instead of self.field.widget
        id_ = self.widget.attrs.get("id") or self.auto_id
        return self.widget.id_for_label(id_)

    @cached_property
    def initial(self) -> Any:
        # Use self.widget instead of self.field.widget
        if django.VERSION >= (4, 0):
            return self.form.get_initial_for_field(self.field, self.name)
        else:
            data = self.form.get_initial_for_field(self.field, self.name)
            # If this is an auto-generated default date, nix the microseconds for
            # standardized handling. See #22502.
            if (isinstance(data, (datetime.datetime, datetime.time)) and
                    not self.widget.supports_microseconds):
                data = data.replace(microsecond=0)
            return data
