from django.test import TestCase
from django.urls import reverse


class TestTemplate(TestCase):
    def test_sobre_page_template_used(self):
        view_path = reverse("dashboard:sobre")
        response = self.client.get(view_path)
        return self.assertTemplateUsed(response, "base.html")
