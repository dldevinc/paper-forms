from django import forms

from paper_forms.composers.bootstrap4 import Bootstrap4


class ExampleForm(forms.Form):
    use_required_attribute = False
    error_css_class = "is-invalid"

    char = forms.CharField()
    number = forms.IntegerField(
        initial=18
    )
    email = forms.EmailField(
        required=False
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput
    )
    url = forms.URLField(
        required=False
    )
    text = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    # selects
    select = forms.ChoiceField(
        choices=(
            ("r", "Red"),
            ("g", "Green"),
            ("b", "Blue"),
        ),
    )
    select_multiple = forms.MultipleChoiceField(
        required=False,
        choices=(
            ("read", "Read"),
            ("write", "Write"),
            ("execute", "Execute"),
        ),
        initial=["read", "execute"],
        widget=forms.SelectMultiple,
    )

    # files
    file = forms.FileField(
        required=False
    )
    image = forms.ImageField(
        required=False
    )

    # checkboxes
    checkbox = forms.BooleanField()
    custom_checkbox = forms.BooleanField(
        required=False,
    )
    checkbox_multiple = forms.TypedMultipleChoiceField(
        required=False,
        coerce=int,
        choices=(
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ),
        widget=forms.CheckboxSelectMultiple,
    )
    custom_checkbox_multiple = forms.MultipleChoiceField(
        required=False,
        choices=(
            ("en", "English"),
            ("es", "Spanish"),
            ("ja", "Japanese"),
        ),
        widget=forms.CheckboxSelectMultiple,
    )

    # radios
    radio = forms.ChoiceField(
        initial="male",
        choices=(
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ),
        widget=forms.RadioSelect,
    )
    custom_radio = forms.TypedChoiceField(
        coerce=int,
        choices=(
            (0, "HTML"),
            (1, "CSV"),
            (2, "Text"),
        ),
        initial=1,
        widget=forms.RadioSelect,
    )

    # hidden & readonly
    honeypot = forms.CharField(
        required=True,
        widget=forms.HiddenInput,
        initial="honey"
    )
    readonly = forms.CharField(
        required=False,
        label="Readonly field"
    )

    class Composer(Bootstrap4):
        template_names = {
            "custom_checkbox": "paper_forms/bootstrap4/custom_checkbox.html",
            "custom_checkbox_multiple": "paper_forms/bootstrap4/custom_checkbox_select.html",
            "custom_radio": "paper_forms/bootstrap4/custom_radio_select.html",
        }
        labels = {
            "checkbox": "I accept the Terms and Conditions",
        }
        help_texts = {
            "password": "Your password must be 8-20 characters long, contain letters and numbers, "
                        "and must not contain spaces, special characters, or emoji."
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_errors = "add-errors" in self.data

    def clean(self):
        if self.add_errors:
            self.add_error(None, "Form error 1")
            self.add_error(None, "Form error 2")
            self.add_error("char", "Your name is invalid.")
            self.add_error("char", "Your name is too common.")
            self.add_error("password", "Password is too weak.")
            self.add_error("select", "Select a valid color.")
            self.add_error("checkbox_multiple", self.fields["checkbox_multiple"].error_messages["required"])
            self.add_error("radio", "Select a valid choice.")
            self.add_error("custom_radio", "Select a valid choice.")

        return super().clean()
