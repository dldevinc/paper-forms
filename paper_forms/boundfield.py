import copy
import datetime

import django
from django.forms.boundfield import BoundField as _BoundField
from django.forms.boundfield import BoundWidget
from django.utils.functional import cached_property


class BoundField(_BoundField):
    def __init__(self, form, field, name, composer):
        super().__init__(form, field, name)
        self.composer = composer

    def get_template_name(self, widget):
        if widget.is_hidden:
            # default template
            return widget.template_name

        composer_template_names = self.composer.template_names
        if composer_template_names and self.name in composer_template_names:
            return composer_template_names[self.name]

        return self.composer.get_default_template_name(widget)

    def get_widget_attrs(self, widget, attrs=None):
        attrs = attrs or {}
        attrs = self.build_widget_attrs(attrs, widget)

        composer_css_classes = attrs.pop("class", self.composer.get_default_css_classes(widget))
        composer_css_classes = self.css_classes(composer_css_classes)
        if composer_css_classes:
            attrs["class"] = composer_css_classes

        return self.composer.build_widget_attrs(widget, attrs)

    def get_context(self, widget, attrs=None, only_initial=False):
        context = widget.get_context(
            name=self.html_initial_name if only_initial else self.html_name,
            value=self.value(),
            attrs=attrs
        )

        context["errors"] = self.errors

        composer_labels = self.composer.labels
        if composer_labels and self.name in composer_labels:
            context["label"] = composer_labels[self.name]
        else:
            context["label"] = self.label

        composer_help_texts = self.composer.help_texts
        if composer_help_texts and self.name in composer_help_texts:
            context["help_text"] = composer_help_texts[self.name]
        else:
            context["help_text"] = self.help_text

        return self.composer.build_widget_context(widget, context)

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        widget = widget or self.widget
        if self.field.localize:
            widget.is_localized = True

        attrs = self.get_widget_attrs(widget, attrs)
        if self.auto_id and "id" not in widget.attrs:
            attrs.setdefault("id", self.html_initial_id if only_initial else self.auto_id)

        context = self.get_context(widget, attrs, only_initial=only_initial)

        return widget._render(
            template_name=self.get_template_name(widget),
            context=context,
            renderer=self.composer.get_renderer(self.form),
        )

    @cached_property
    def widget(self):
        composer_widgets = self.composer.widgets
        if composer_widgets and self.name in composer_widgets:
            widget = composer_widgets[self.name]
            if isinstance(widget, type):
                widget = widget()
            else:
                widget = copy.deepcopy(widget)
            return widget

        return self.field.widget

    @cached_property
    def subwidgets(self):
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
    def data(self):
        # Use self.widget instead of self.field.widget
        if django.VERSION >= (4, 0):
            return self.form._widget_data_value(self.widget, self.html_name)
        else:
            return self.widget.value_from_datadict(
                self.form.data, self.form.files, self.html_name
            )

    @property
    def is_hidden(self):
        # Use self.widget instead of self.field.widget
        return self.widget.is_hidden

    @property
    def id_for_label(self):
        # Use self.widget instead of self.field.widget
        id_ = self.widget.attrs.get("id") or self.auto_id
        return self.widget.id_for_label(id_)

    @cached_property
    def initial(self):
        # Use self.widget instead of self.field.widget
        data = self.form.get_initial_for_field(self.field, self.name)
        if django.VERSION < (4, 0):
            # If this is an auto-generated default date, nix the microseconds for
            # standardized handling. See #22502.
            if (isinstance(data, (datetime.datetime, datetime.time)) and
                    not self.widget.supports_microseconds):
                data = data.replace(microsecond=0)
        return data
