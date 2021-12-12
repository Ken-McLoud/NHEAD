from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import os.path
from django.conf import settings
from shutil import copyfile
from pathlib import Path


def prepend_new_lines(lines):
    return ["\n" + line for line in lines]


def check_imports(filepath, imports):
    for import_str in imports:
        if not line_in_file(filepath, import_str):
            prepend_to_file(filepath, import_str)


def line_in_file(filepath, line):
    with open(filepath, "r") as myf:
        return line in myf.read()


def prepend_to_file(filepath, line):
    with open(filepath, "r") as myf:
        old_file = myf.read()
    with open(filepath, "w") as myf:
        myf.write(line + "\r")
        myf.write(old_file)


def make_name(model_name, prefix, suffix):
    if model_name.lower().endswith("model"):
        return prefix + model_name[:-5] + suffix
    else:
        return prefix + model_name + suffix


def get_fields_list(fields):
    """
    take the list of field objects from the model
    return a list of strings which represent the field names
    to include in the form
    """
    fields_to_exclude = ["id", "created", "modified"]
    return [f.name for f in fields if f.name not in fields_to_exclude]


def get_fields_dict(fields, obj):
    """
    take the list of field objects from the model
    return a list of dicts of name,value pairs
    to include in the list view
    """
    fields_to_exclude = ["id", "created", "modified"]
    d = []
    for field in fields:
        if field.name not in fields_to_exclude:
            d.append({"name": field.name, "value": str(field.value_from_object(obj))})


class Command(BaseCommand):
    help = "Auto populates CRUD pages for a model"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("model_name", type=str)

    def handle(self, *args, **options):
        self.make_names(app_name=options["app_name"], model_name=options["model_name"])
        try:
            self.get_model()
        except Exception:
            return "Model could not be found"
        self.make_sure_urls_exists()
        self.make_form()
        self.make_create()
        self.make_detail()
        self.make_list()
        self.make_edit()
        self.make_delete()
        self.stdout.write("Done")

    def get_model(self):
        models = apps.get_models()
        key_str = self.app_name + ".models." + self.model_name
        try:
            self.model = [m for m in models if key_str in str(m)][0]
        except IndexError:
            raise Exception("Model could not be found")
        self.fields = self.model._meta.fields

    def make_sure_urls_exists(self):
        if not os.path.isfile(self.urls_path):
            with open(self.urls_path, "w") as myf:
                myf.write("from django.urls import path\r")
                myf.write("from . import views\r")
                myf.write("urlpatterns = []\r")

    def make_names(self, app_name="", model_name=""):
        self.app_name = app_name
        self.model_name = model_name
        self.name = make_name(self.model_name, "", "")
        self.forms_path = os.path.join(settings.BASE_DIR, self.app_name, "forms.py")
        self.urls_path = os.path.join(settings.BASE_DIR, self.app_name, "urls.py")
        self.views_path = os.path.join(settings.BASE_DIR, self.app_name, "views.py")
        self.tests_path = os.path.join(settings.BASE_DIR, self.app_name, "tests.py")
        self.templates_path = os.path.join(
            settings.BASE_DIR, self.app_name, "templates", self.app_name, ""
        )
        self.form_name = make_name(self.model_name, "", "Form")
        self.create_view_name = make_name(self.model_name, "Create", "View")
        self.create_url_name = self.create_view_name[:-4].lower()
        self.detail_view_name = make_name(self.model_name, "Detail", "View")
        self.detail_url_name = self.model_name.lower()
        self.list_view_name = make_name(self.model_name, "List", "View")
        self.list_url_name = f"{self.model_name.lower()}s"
        self.edit_view_name = make_name(self.model_name, "Edit", "View")
        self.edit_url_name = self.edit_view_name[:-4].lower()
        self.delete_view_name = make_name(self.model_name, "Delete", "View")
        self.delete_url_name = self.delete_view_name[:-4].lower()

    def make_form(self):
        def get_fieldset_args():
            """return a string to pass to fieldset"""
            args = [""] + get_fields_list(self.fields)
            return f"{args}"[1:-1]

        imports = [
            "from django.forms import ModelForm",
            "from crispy_forms.helper import FormHelper",
            f"from .models import {self.model_name}",
            "from crispy_forms.layout import Submit, Layout, Fieldset",
            "from crispy_forms.bootstrap import FormActions",
        ]
        check_imports(self.forms_path, imports)
        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.form_name}(ModelForm):",
                "\tdef __init__(self, *args, **kwargs):",
                "\t\tsuper().__init__(*args, **kwargs)",
                "\t\tself.helper = FormHelper()",
                '\t\tself.helper.form_method = "post"',
                f"\t\tself.helper.layout=Layout(Fieldset({get_fieldset_args()}))",
                '\t\tself.helper.layout.append(FormActions(Submit("done", "Done")))',
                "",
                "\tclass Meta:",
                f"\t\tmodel = {self.model_name}",
                f"\t\tfields = {get_fields_list(self.fields)}",
            ]
        )
        self.write_if_needed(self.forms_path, code, name="form")

    def make_create(self):
        try:
            self.add_to_urls(self.create_view_name, self.create_url_name)
        except Exception:
            self.stdout.write("Create View not created, one already existed in urls")
            return
        self.add_create_view_code()
        self.copy_template("form.html", f"{self.model_name}_form.html")
        self.make_view_tests(
            view_name=self.create_view_name, url_name=self.create_url_name
        )

    def make_detail(self):
        try:
            self.add_to_urls(
                self.detail_view_name, self.detail_url_name, url_args="/<int:pk>"
            )
        except Exception as e:
            print(e)
            self.stdout.write("Detail View not created, one already existed in urls")
            return
        self.add_detail_view_code()
        self.copy_template("detail.html", f"{self.model_name}_detail.html")
        # todo, saving this for later
        # need to create an object in the database in order to test this
        # but don't have a good way of making default values for arbitrary required fields
        # self.make_view_tests(
        #     view_name=self.detail_view_name,
        #     url_name=self.detail_url_name,
        #     needs_pk=True
        # )

    def make_list(self):
        try:
            self.add_to_urls(self.list_view_name, self.list_url_name)
        except Exception:
            self.stdout.write("List View not created, one already existed in urls")
            return
        self.add_list_view_code()
        self.copy_template("list.html", f"{self.model_name}_list.html")
        self.make_view_tests(view_name=self.list_view_name, url_name=self.list_url_name)

    def make_edit(self):
        try:
            self.add_to_urls(
                self.edit_view_name, self.edit_url_name, url_args="/<int:pk>"
            )
        except Exception:
            self.stdout.write("Edit View not created, one already existed in urls")
            return
        self.add_edit_view_code()
        self.copy_template("form.html", f"{self.model_name}_form.html")
        # todo, saving this for later
        # need to create an object in the database in order to test this
        # but don't have a good way of making default values for arbitrary required fields
        # self.make_view_tests(
        #     view_name=self.edit_view_name,
        #     url_name=self.edit_url_name,
        #     needs_pk=True
        # )

    def make_delete(self):
        try:
            self.add_to_urls(
                self.delete_view_name, self.delete_url_name, url_args="/<int:pk>"
            )
        except Exception:
            self.stdout.write("Delete View not created, one already existed in urls")
            return
        self.add_delete_view_code()
        self.copy_template("delete.html", f"{self.model_name}_confirm_delete.html")
        # todo, saving this for later
        # need to create an object in the database in order to test this
        # but don't have a good way of making default values for arbitrary required fields
        # self.make_view_tests(
        #     view_name=self.edit_view_name,
        #     url_name=self.edit_url_name,
        #     needs_pk=True
        # )

    def write_if_needed(self, filepath, lines, key_line=1, name=""):
        """check to see if lines[key_line] is already in file
        if so, print out message using name, that nothing was written
        if not, write lines to the the end of file
        """
        if line_in_file(filepath, lines[1]):
            self.stdout.write(f"{name} not created, one already existed")
            return
        with open(filepath, "a") as myf:
            myf.writelines(lines)

    def add_to_urls(self, view_name, url_name, url_args=""):
        if not line_in_file(self.urls_path, f"views.{view_name}"):
            code = prepend_new_lines(
                [
                    "\n#added by autocrud",
                    f'urlpatterns.append(path("{url_name}{url_args}", views.{view_name}.as_view(), name="{url_name}"))',
                ]
            )
            self.write_if_needed(self.urls_path, code, name="url")
        else:
            raise Exception(f"{view_name} already in urls.py")

    def add_create_view_code(self):
        imports = [
            "from django.views.generic.edit import CreateView",
            "from django.contrib.auth.mixins import LoginRequiredMixin",
            f"from .models import {self.model_name}",
            f"from .forms import {self.form_name}",
            "from django.urls import reverse_lazy",
        ]
        check_imports(self.views_path, imports)

        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.create_view_name}(LoginRequiredMixin, CreateView):",
                '\tlogin_url = "/login"',
                f"\tmodel = {self.model_name}",
                f"\tform_class = {self.form_name}",
                "",
                "\tdef get_context_data(self):",
                "\t\tcontext = super().get_context_data()",
                f'\t\tcontext["page_title"] = "Create a new {self.name}"',
                f'\t\tcontext["app_name"] = "{self.app_name}"',
                f'\t\tcontext["breadcrumbs"] = ["Create a new {self.name}"]',
                "\t\treturn context",
                "",
                "\tdef get_success_url(self):",
                f"\t\treturn reverse_lazy('{self.app_name}:{self.detail_url_name}',kwargs={{'pk':self.object.pk}})",
            ]
        )
        self.write_if_needed(self.views_path, code, name="Create View")

    def copy_template(self, template_name, final_name):
        """copy template_name from the commands folder to the appropriate template folder"""
        if not Path(self.templates_path).is_dir():
            os.makedirs(self.templates_path)
        src = os.path.join(Path(__file__).resolve().parent, template_name)
        dst = os.path.join(self.templates_path, final_name.lower())
        copyfile(src, dst)

    def make_view_tests(self, view_name="", url_name="", needs_pk=False):
        # todo this needs to work with any view, not just create
        imports = [
            "from django.test import TestCase, RequestFactory",
            f"from .models import {self.model_name}",
            "from django.urls import reverse",
            "from django.contrib.auth.models import AnonymousUser, User",
            f"from .views import {view_name}",
        ]
        check_imports(self.tests_path, imports)
        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.model_name}{url_name}Tests(TestCase):",
                "\tdef setUp(self):",
                "\t\tself.factory = RequestFactory()",
                "\t\tself.user = User.objects.create_user(username='user', password='top_secret')",
                "",
                f"\tdef test_{url_name}_responds_logged_in(self):",
                f"\t\trequest = self.factory.get(reverse('{self.app_name}:{url_name}'))",
                "\t\trequest.user=self.user",
                f"\t\tresponse = {view_name}.as_view()(request)",
                "\t\tself.assertEqual(response.status_code, 200)",
                "",
                f"\tdef test_{url_name}_responds_not_logged_in(self):",
                f"\t\trequest = self.factory.get(reverse('{self.app_name}:{url_name}'))",
                "\t\trequest.user=AnonymousUser()",
                f"\t\tresponse = {view_name}.as_view()(request)",
                "\t\tself.assertEqual(response.status_code, 302)",
            ]
        )
        self.write_if_needed(self.tests_path, code, name=f"{url_name} Tests")

    def add_detail_view_code(self):
        imports = [
            "from django.views.generic import DetailView",
            "from django.contrib.auth.mixins import LoginRequiredMixin",
            f"from .models import {self.model_name}",
        ]
        check_imports(self.views_path, imports)

        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.detail_view_name}(LoginRequiredMixin, DetailView):",
                '\tlogin_url = "/login"',
                f"\tmodel = {self.model_name}",
                "",
                "\tdef get_context_data(self,object):",
                "\t\tcontext = super().get_context_data()",
                f'\t\tcontext["model_name"] = "{self.name}"',
                f'\t\tcontext["app_name"] = "{self.app_name}"',
                f'\t\tcontext["list_view_url"] = "{self.app_name}:{self.list_url_name}"',
                "\t\treturn context",
            ]
        )
        self.write_if_needed(self.views_path, code, name="Detail View")

    def add_list_view_code(self):
        imports = [
            "from django.views.generic import ListView",
            "from django.contrib.auth.mixins import LoginRequiredMixin",
            f"from .models import {self.model_name}",
        ]
        check_imports(self.views_path, imports)

        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.list_view_name}(LoginRequiredMixin, ListView):",
                '\tlogin_url = "/login"',
                f"\tmodel = {self.model_name}",
                "\tpaginate_by = 20",
                f"\tqueryset={self.model_name}.objects.all().order_by('pk')",
                "",
                "\tdef get_context_data(self):",
                "\t\tcontext = super().get_context_data()",
                f'\t\tcontext["model_name"] = "{self.name}"',
                f'\t\tcontext["app_name"] = "{self.app_name}"',
                f'\t\tcontext["detail_url_name"] = "{self.app_name}:{self.detail_url_name}"',
                f'\t\tcontext["edit_url_name"] = "{self.app_name}:{self.edit_url_name}"',
                f'\t\tcontext["delete_url_name"] = "{self.app_name}:{self.delete_url_name}"',
                f'\t\tcontext["fields"] = {get_fields_list(self.fields)}',
                '\t\tcontext[\'header\']=[\'ID #\']+context["fields"]+["",""]',
                "\t\ttable=[]",
                "\t\tfor obj in context['object_list']:",
                "\t\t\ttable.append({'pk':obj.pk,'fields':[self.get_field_value(obj,field) for field in context['fields']],})",
                "\t\tcontext['table']=table",
                "\t\treturn context",
                "",
                "\tdef get_field_value(self,obj,field_name):",
                "\t\tfor field in obj._meta.fields:",
                "\t\t\tif field.name!=field_name:",
                "\t\t\t\tcontinue",
                "\t\t\treturn field.value_from_object(obj)",
            ]
        )

        self.write_if_needed(self.views_path, code, name="List View")

    def add_edit_view_code(self):
        imports = [
            "from django.views.generic import UpdateView",
            "from django.contrib.auth.mixins import LoginRequiredMixin",
            f"from .models import {self.model_name}",
            f"from .forms import {self.form_name}",
        ]
        check_imports(self.views_path, imports)

        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.edit_view_name}(LoginRequiredMixin, UpdateView):",
                '\tlogin_url = "/login"',
                f"\tmodel = {self.model_name}",
                f"\tform_class = {self.form_name}",
                "",
                "\tdef get_context_data(self, **kwargs):",
                "\t\tcontext = super().get_context_data()",
                f'\t\tcontext["model_name"] = "{self.name}"',
                f'\t\tcontext["app_name"] = "{self.app_name}"',
                "\t\treturn context",
                "",
                "\tdef get_success_url(self):",
                f"\t\treturn reverse_lazy('{self.app_name}:{self.detail_url_name}',kwargs={{'pk':self.object.pk}})",
            ]
        )
        self.write_if_needed(self.views_path, code, name="Edit View")

    def add_delete_view_code(self):
        imports = [
            "from django.views.generic import DeleteView",
            "from django.contrib.auth.mixins import LoginRequiredMixin",
            f"from .models import {self.model_name}",
        ]
        check_imports(self.views_path, imports)

        code = prepend_new_lines(
            [
                "\n#added by autocrud",
                f"class {self.delete_view_name}(LoginRequiredMixin, DeleteView):",
                '\tlogin_url = "/login"',
                f"\tmodel = {self.model_name}",
                f'\tsuccess_url = reverse_lazy("{self.app_name}:{self.list_url_name}")',
                "",
                "\tdef get_context_data(self,object):",
                "\t\tcontext = super().get_context_data()",
                f'\t\tcontext["model_name"] = "{self.name}"',
                f'\t\tcontext["app_name"] = "{self.app_name}"',
                f'\t\tcontext["list_view_url"] = "{self.app_name}:{self.list_url_name}"',
                "\t\treturn context",
            ]
        )
        self.write_if_needed(self.views_path, code, name="Edit View")
