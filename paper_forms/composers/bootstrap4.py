from django.forms import Widget, widgets

from .base import BaseComposer


class Bootstrap4(BaseComposer):
    def get_default_template_name(self, name: str, widget: Widget) -> str:
        if isinstance(widget, widgets.CheckboxInput):
            return "paper_forms/bootstrap4/checkbox.html"
        elif isinstance(widget, widgets.CheckboxSelectMultiple):
            return "paper_forms/bootstrap4/checkbox_select.html"
        elif isinstance(widget, widgets.RadioSelect):
            return "paper_forms/bootstrap4/radio_select.html"
        elif isinstance(widget, widgets.FileInput):
            return "paper_forms/bootstrap4/file.html"
        else:
            return "paper_forms/bootstrap4/input.html"

    def build_widget_attrs(self, name: str, attrs: dict, widget: Widget) -> dict:
        attrs = super().build_widget_attrs(name, attrs, widget)
        classes = set(attrs.pop("class", "").split())

        if isinstance(widget, widgets.CheckboxInput):
            classes.add("form-check-input")
        elif isinstance(widget, widgets.CheckboxSelectMultiple):
            classes.add("form-check-input")
        elif isinstance(widget, widgets.RadioSelect):
            classes.add("form-check-input")
        elif isinstance(widget, widgets.Select):
            classes.add("custom-select")
        elif isinstance(widget, widgets.FileInput):
            classes.add("custom-file-input")
        else:
            classes.add("form-control")

        attrs["class"] = " ".join(classes)
        return attrs
