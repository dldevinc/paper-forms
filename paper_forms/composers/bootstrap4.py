from django.forms import widgets

from .base import BaseComposer


class Bootstrap4(BaseComposer):
    def get_default_template_name(self, widget):
        if isinstance(widget, widgets.CheckboxInput):
            return "paper_forms/bootstrap4/checkbox.html"
        elif isinstance(widget, widgets.RadioSelect):
            return "paper_forms/bootstrap4/radio_select.html"
        elif isinstance(widget, widgets.CheckboxSelectMultiple):
            return "paper_forms/bootstrap4/checkbox_select.html"
        elif isinstance(widget, widgets.FileInput):
            return "paper_forms/bootstrap4/file.html"
        else:
            return "paper_forms/bootstrap4/input.html"

    def get_default_css_classes(self, widget):
        if isinstance(widget, widgets.CheckboxInput):
            return "form-check-input"
        elif isinstance(widget, widgets.RadioSelect):
            return "form-check-input"
        elif isinstance(widget, widgets.CheckboxSelectMultiple):
            return "form-check-input"
        elif isinstance(widget, widgets.Select):
            return "custom-select"
        elif isinstance(widget, widgets.FileInput):
            return "custom-file-input"
        else:
            return "form-control"
