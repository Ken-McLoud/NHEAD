from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse, reverse_lazy, resolve
from django.test import TestCase, RequestFactory, Client
import random
from django.contrib.sessions.middleware import SessionMiddleware


def url_resonpds(url_pattern="", login_required=False):
    """
    a general purpose function for making sure a url pattern responds with a 200
    """
    url = reverse(url_pattern)
    factory = RequestFactory()
    user = User.objects.create_user(
        username=f"user{int(random.random()*1e6)}", password="top_secret"
    )
    request = factory.get(url)
    if login_required:
        request.user = user
    else:
        request.user = AnonymousUser()
    middleware = SessionMiddleware(request)
    middleware.process_request(request)
    request.session.save()
    view, args, kwargs = resolve(url)
    kwargs["request"] = request
    response = view(*args, **kwargs)
    return response.status_code in [200, 302]


class PingUrlsTest(TestCase):
    """
    a general purpose test for making sure a url pattern responds with a 200
    """

    login_not_required_urls = [
        "base_app:home",
        "base_app:login",
        "base_app:password_reset",
        "base_app:password_reset_done",
        "base_app:password_reset_complete",
    ]
    login_required_urls = ["base_app:logout"]

    def test_urls_respond(self):
        for url_pattern in self.login_not_required_urls:
            self.assertTrue(
                url_resonpds(
                    url_pattern=url_pattern,
                ),
                msg=f"{url_pattern} did not respond",
            )
        for url_pattern in self.login_required_urls:
            self.assertTrue(
                url_resonpds(
                    url_pattern=url_pattern,
                    login_required=False,
                ),
                msg=f"{url_pattern} did not respond",
            )
