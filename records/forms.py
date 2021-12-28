from .models import KidModel
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import HTML, Div, Field, Submit, Layout, Fieldset
from .models import FamilyModel
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms


# added by autocrud
class FamilyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs = self.clean_kwargs(kwargs)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                "name",
                "zip_code",
                "user",
            )
        )
        self.helper.layout.append(
            Div(FormActions(Submit("done", self.btn_text)), css_class="mt-3")
        )

    def clean_kwargs(self, kwargs):
        if "btn_text" in kwargs:
            self.btn_text = kwargs["btn_text"]
            del kwargs["btn_text"]
        else:
            self.btn_text = "Add kids"
        return kwargs

    def clean_zip_code(self):
        data = self.cleaned_data["zip_code"]
        if len(data) != 5:
            raise ValidationError("Zip Code must be 5 digits long")
        if not data.isdigit():
            raise ValidationError("Zip Code must only contain numbers")
        return data

    class Meta:
        model = FamilyModel
        fields = ["name", "zip_code", "user"]
        widgets = {
            "user": forms.HiddenInput(),
        }
        labels = {"name": "Name <br>(Will be public, so feel free to use an alias)"}


# added by autocrud
class KidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "records:createkid"
        self.helper.layout = Layout(Fieldset("", "family", "birth_year", "gender"))
        self.helper.layout.append(
            FormActions(
                Submit("add", "Add another kid"),
                HTML(
                    """
                <a href="/records/myfamily" class="btn btn-primary">Done adding kids</a>
                """
                ),
                css_class="mt-3",
            )
        )
        self.fields["gender"].required = False

    class Meta:
        model = KidModel
        fields = ["family", "birth_year", "gender"]
        widgets = {
            "family": forms.HiddenInput(),
        }
