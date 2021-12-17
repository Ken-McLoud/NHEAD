from .views import ListKidView
from .views import CreateKidView
from .models import KidModel
from .views import ListFamilyView
from .views import CreateFamilyView
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from .models import FamilyModel
from django.test import TestCase, RequestFactory


# Create your tests here.


# added by autocrud
class FamilyModelcreatefamilyTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="user", password="top_secret")

    def test_createfamily_responds_logged_in(self):
        request = self.factory.get(reverse("records:createfamily"))
        request.user = self.user
        response = CreateFamilyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_createfamily_responds_not_logged_in(self):
        request = self.factory.get(reverse("records:createfamily"))
        request.user = AnonymousUser()
        response = CreateFamilyView.as_view()(request)
        self.assertEqual(response.status_code, 302)


# added by autocrud
class FamilyModelfamilymodelsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="user", password="top_secret")

    def test_familymodels_responds_logged_in(self):
        request = self.factory.get(reverse("records:familymodels"))
        request.user = self.user
        response = ListFamilyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_familymodels_responds_not_logged_in(self):
        request = self.factory.get(reverse("records:familymodels"))
        request.user = AnonymousUser()
        response = ListFamilyView.as_view()(request)
        self.assertEqual(response.status_code, 302)


# added by autocrud
class KidModelcreatekidTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="user", password="top_secret")

    def test_createkid_responds_logged_in(self):
        request = self.factory.get(reverse("records:createkid"))
        request.user = self.user
        response = CreateKidView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_createkid_responds_not_logged_in(self):
        request = self.factory.get(reverse("records:createkid"))
        request.user = AnonymousUser()
        response = CreateKidView.as_view()(request)
        self.assertEqual(response.status_code, 302)


# added by autocrud
class KidModelkidmodelsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="user", password="top_secret")

    def test_kidmodels_responds_logged_in(self):
        request = self.factory.get(reverse("records:kidmodels"))
        request.user = self.user
        response = ListKidView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_kidmodels_responds_not_logged_in(self):
        request = self.factory.get(reverse("records:kidmodels"))
        request.user = AnonymousUser()
        response = ListKidView.as_view()(request)
        self.assertEqual(response.status_code, 302)
