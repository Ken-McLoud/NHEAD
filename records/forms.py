from django.urls.base import reverse_lazy
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
        if self.has_family_pk:
            self.helper.form_action = reverse_lazy(
                "records:editfamily",
                kwargs={"pk": self.family_pk},
            )
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
            self.btn_text = "Done"
        if "family_pk" in kwargs:
            self.family_pk = kwargs["family_pk"]
            del kwargs["family_pk"]
            self.has_family_pk = True
        else:
            self.has_family_pk = False
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
    form_type = forms.CharField(
        max_length=200,
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "records:createkid"
        self.helper.layout = Layout(Fieldset("", "family", "birth_year", "gender"))
        self.helper.layout.append(
            FormActions(
                Submit("done", "Done"),
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
