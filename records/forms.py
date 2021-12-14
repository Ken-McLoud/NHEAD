from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Fieldset
from .models import FamilyModel
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.core.exceptions import ValidationError


# added by autocrud
class FamilyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(Fieldset("", "name", "zip_code"))
        self.helper.layout.append(FormActions(Submit("done", "Done")))

    def clean_zip_code(self):
        data = self.cleaned_data["zip_code"]
        if len(data) != 5:
            raise ValidationError("Zip Code must be 5 digits long")
        if not data.isdigit():
            raise ValidationError("Zip Code must only contain numbers")
        return data

    class Meta:
        model = FamilyModel
        fields = ["name", "zip_code"]
