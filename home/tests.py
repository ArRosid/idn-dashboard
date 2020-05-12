from django.test import TestCase
from django.urls import reverse, resolve
from home.views import home


class HomeTests(TestCase):
    def setUp(self):
        self.url = reverse("home:home")

    def test_home_view_status_code(self):
        """
            Test the return status code of home page
        """
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_home_view(self):
        """
            Test the home view
        """

        view = resolve(self.url)
        self.assertEqual(view.func, home)
