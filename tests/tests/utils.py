from paper_forms.boundfield import BoundField
from paper_forms.utils import get_composer


def get_bound_field(form, name):
    return BoundField(form, form.fields[name], name, get_composer(form))
