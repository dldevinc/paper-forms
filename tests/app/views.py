from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ExampleForm


class DjangoView(FormView):
    form_class = ExampleForm
    success_url = reverse_lazy("app:django")
    template_name = "app/index.html"

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, "Form valid")
        return super().form_valid(form)


class JinjaView(FormView):
    template_engine = "jinja2"
    form_class = ExampleForm
    success_url = reverse_lazy("app:jinja2")
    template_name = "app/index.html"

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Form valid')
        return super().form_valid(form)
