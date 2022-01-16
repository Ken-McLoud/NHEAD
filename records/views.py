from django.http import request
from django.http.response import HttpResponse
from django.utils.html import conditional_escape
from django.views.generic.base import RedirectView
from .forms import KidForm
from .models import KidModel
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .forms import FamilyForm
from .models import FamilyModel
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.


# added by autocrud
class CreateFamilyView(LoginRequiredMixin, CreateView):
    login_url = "/accounts/login"
    model = FamilyModel
    form_class = FamilyForm
    template_name = "records/simple_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["page_title"] = "Create a new Family"
        context["app_name"] = "records"
        context["breadcrumbs"] = ["Create a new Family"]
        context["header"] = "Create a Family Entry"
        context["sub_header"] = "This will help you connect with other local families"
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["user"] = self.request.user
        return initial

    def get_success_url(self):
        return reverse_lazy("records:myfamily")


# added by autocrud
class DetailFamilyView(LoginRequiredMixin, DetailView):
    login_url = "/accounts/login"
    model = FamilyModel

    def get_context_data(self, object):
        context = super().get_context_data()
        context["model_name"] = "Family"
        context["app_name"] = "records"
        context["list_view_url"] = "records:familymodels"
        context["header"] = f"{object.name} Family"
        context["sub_header"] = "Details"
        context["kids"] = KidModel.objects.filter(family=object)
        return context


# added by autocrud
class ListFamilyView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
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
    login_url = "/accounts/login"
    model = FamilyModel
    form_class = FamilyForm
    template_name = "records/simple_form.html"

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["btn_text"] = "Done"
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["model_name"] = "Family"
        context["app_name"] = "records"
        context["header"] = "Modify Your Family Entry"
        context["sub_header"] = "This will help you connect with other local families"
        return context

    def get_success_url(self):
        return reverse_lazy("records:familymodel", kwargs={"pk": self.object.pk})


# added by autocrud
class DeleteFamilyView(UserPassesTestMixin, DeleteView):
    login_url = "/accounts/login"
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


@login_required(login_url="/accounts/login")
def createkidview(http_request):
    form = KidForm(http_request.POST)
    if form.is_valid():
        form.save()
    return redirect("records:myfamily")


@login_required(login_url="/accounts/login")
def editfamilyview(http_request, pk):
    family = FamilyModel.objects.get(pk=pk)
    form = FamilyForm(http_request.POST, family_pk=pk, instance=family)
    if form.is_valid():
        form.save()
    return redirect("records:myfamily")


# added by autocrud
class DetailKidView(LoginRequiredMixin, DetailView):
    login_url = "/accounts/login"
    model = KidModel

    def get_context_data(self, object):
        context = super().get_context_data()
        context["model_name"] = "Kid"
        context["app_name"] = "records"
        context["list_view_url"] = "records:kidmodels"
        return context


# added by autocrud
class ListKidView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    model = KidModel
    paginate_by = 20
    queryset = KidModel.objects.all().order_by("pk")

    def get_context_data(self):
        context = super().get_context_data()
        context["model_name"] = "Kid"
        context["app_name"] = "records"
        context["detail_url_name"] = "records:kidmodel"
        context["edit_url_name"] = "records:editkid"
        context["delete_url_name"] = "records:deletekid"
        context["fields"] = ["family", "birth_year"]
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
class EditKidView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login"
    model = KidModel
    form_class = KidForm
    template_name = "records/simple_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["model_name"] = "Kid"
        context["app_name"] = "records"
        return context

    def get_success_url(self):
        return reverse_lazy("records:kidmodel", kwargs={"pk": self.object.pk})


# added by autocrud
class DeleteKidView(LoginRequiredMixin, DeleteView):
    login_url = "/accounts/login"
    model = KidModel
    success_url = reverse_lazy("records:myfamily")

    def get_context_data(self, object):
        context = super().get_context_data()
        context["model_name"] = "Kid"
        context["app_name"] = "records"
        context["list_view_url"] = "records:kidmodels"

        return context


def inline_add_kid(http_request, family_pk):
    context = {
        "form": KidForm(initial={"family": FamilyModel.objects.get(pk=family_pk)}),
        "header": "New Kid:",
    }
    return render(http_request, "records/inline_form.html", context=context)


def inline_edit_family(http_request, family_pk):
    family = FamilyModel.objects.get(pk=family_pk)
    context = {
        "form": FamilyForm(
            initial={
                "name": family.name,
                "zip_code": family.zip_code,
                "user": family.user,
            },
            family_pk=family.pk,
        ),
        "header": "Edit Family:",
    }
    return render(http_request, "records/inline_form.html", context=context)


class MyFamilyView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    login_url = "/accounts/login"

    def get_redirect_url(self, *args, **kwargs):
        try:
            family = FamilyModel.objects.get(user=self.request.user)
            return reverse_lazy("records:familymodel", kwargs={"pk": family.pk})
        except FamilyModel.DoesNotExist:
            return reverse_lazy("records:createfamily")
