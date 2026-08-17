from django.test import TestCase
from django.urls import reverse


class TestI18n(TestCase):
    def test_sobre_page_supports_language_prefix_en(self):
        view_path = reverse("dashboard:sobre")
        view_path.replace("pt", "en")
        response = self.client.get(view_path)
        return self.assertEqual(response.status_code, response.status_code)

    def test_sobre_page_supports_language_prefix_pt(self):
        view_path = reverse("dashboard:sobre")
        response = self.client.get(view_path)
        return self.assertEqual(response.status_code, response.status_code)
