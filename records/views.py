from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .forms import FamilyForm
from .models import FamilyModel
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render

# Create your views here.


# added by autocrud
class CreateFamilyView(LoginRequiredMixin, CreateView):
    login_url = "accounts/login"
    model = FamilyModel
    form_class = FamilyForm

    def get_context_data(self):
        context = super().get_context_data()
        context["page_title"] = "Create a new Family"
        context["app_name"] = "records"
        context["breadcrumbs"] = ["Create a new Family"]
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["user"] = self.request.user
        return initial

    def get_success_url(self):
        return reverse_lazy("records:familymodel", kwargs={"pk": self.object.pk})


# added by autocrud
class DetailFamilyView(LoginRequiredMixin, DetailView):
    login_url = "accounts/login"
    model = FamilyModel

    def get_context_data(self, object):
        context = super().get_context_data()
        context["model_name"] = "Family"
        context["app_name"] = "records"
        context["list_view_url"] = "records:familymodels"
        return context


# added by autocrud
class ListFamilyView(LoginRequiredMixin, ListView):
    login_url = "accounts/login"
    model = FamilyModel
    paginate_by = 20
    queryset = FamilyModel.objects.all().order_by("pk")

    def get_context_data(self):
        context = super().get_context_data()
        context["model_name"] = "Family"
        context["app_name"] = "records"
        context["detail_url_name"] = "records:familymodel"
        context["edit_url_name"] = "records:editfamily"
        context["delete_url_name"] = "records:deletefamily"
        context["fields"] = ["name", "zip_code"]
        context["header"] = ["ID #"] + context["fields"] + ["", ""]
        table = []
        for obj in context["object_list"]:
            table.append(
                {
                    "pk": obj.pk,
                    "fields": [
                        self.get_field_value(obj, field) for field in context["fields"]
                    ],
                }
            )
        context["table"] = table
        return context

    def get_field_value(self, obj, field_name):
        for field in obj._meta.fields:
            if field.name != field_name:
                continue
            return field.value_from_object(obj)


# added by autocrud
class EditFamilyView(UserPassesTestMixin, UpdateView):
    login_url = "accounts/login"
    model = FamilyModel
    form_class = FamilyForm

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["model_name"] = "Family"
        context["app_name"] = "records"
        return context

    def get_success_url(self):
        return reverse_lazy("records:familymodel", kwargs={"pk": self.object.pk})


# added by autocrud
class DeleteFamilyView(UserPassesTestMixin, DeleteView):
    login_url = "accounts/login"
    model = FamilyModel
    success_url = reverse_lazy("records:familymodels")

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, object):
        context = super().get_context_data()
        context["model_name"] = "Family"
        context["app_name"] = "records"
        context["list_view_url"] = "records:familymodels"
        return context
