from django import forms
from django.template import engines
from django.core.validators import MinValueValidator, URLValidator


class BookForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100
    )
    author = forms.CharField(
        label="Author",
        max_length=50
    )
    genre = forms.ChoiceField(
        label="Genre",
        choices=[
            ("fiction", "Fiction"),
            ("non-fiction", "Non-Fiction")
        ]
    )
    publication_date = forms.DateField(
        label="Publication Date",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    is_available = forms.BooleanField(
        label="Available in the Library",
        required=False
    )
    rating = forms.DecimalField(
        label="Rating",
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(0)]
    )
    cover_image = forms.ImageField(
        label="Book Cover",
        required=False
    )
    summary = forms.CharField(
        label="Summary",
        widget=forms.Textarea,
        required=False
    )
    pages = forms.IntegerField(
        label="Number of Pages",
        validators=[MinValueValidator(1)]
    )
    email = forms.EmailField(
        label="Contact Email"
    )
    website = forms.URLField(
        label="Author\"s Website",
        validators=[URLValidator(schemes=["http", "https"])]
    )


class TestSeamlessness:
    def test_form_templates(self):
        default_results = {}
        for engine_name in ["django", "jinja2", "django-jinja"]:
            engine = engines[engine_name]
            default_results[engine_name] = self._default_render(engine)

        assert default_results["django"] == default_results["jinja2"]
        assert default_results["jinja2"] == default_results["django-jinja"]

        paper_form_results = {}
        for engine_name in ["django", "jinja2", "django-jinja"]:
            engine = engines[engine_name]
            paper_form_results[engine_name] = self._paper_form_render(engine)

        assert paper_form_results["django"] == paper_form_results["jinja2"]
        assert paper_form_results["jinja2"] == paper_form_results["django-jinja"]

        for engine_name in ["django", "jinja2", "django-jinja"]:
            assert default_results[engine_name] == paper_form_results[engine_name]

    def _default_render(self, engine):
        template = engine.from_string(
            '<form method="post">'
            '{{ form.title }}'
            '{{ form.author }}'
            '{{ form.genre }}'
            '{{ form.publication_date }}'
            '{{ form.is_available }}'
            '{{ form.rating }}'
            '{{ form.cover_image }}'
            '{{ form.summary }}'
            '{{ form.pages }}'
            '{{ form.email }}'
            '{{ form.website }}'
            '</form>'
        )
        return template.render({
            "form": BookForm()
        })

    def _paper_form_render(self, engine):
        template = engine.from_string(
            '<form method="post">'
            '{% field form.title %}'
            '{% field form.author %}'
            '{% field form.genre %}'
            '{% field form.publication_date %}'
            '{% field form.is_available %}'
            '{% field form.rating %}'
            '{% field form.cover_image %}'
            '{% field form.summary %}'
            '{% field form.pages %}'
            '{% field form.email %}'
            '{% field form.website %}'
            '</form>'
        )
        return template.render({
            "form": BookForm()
        })
