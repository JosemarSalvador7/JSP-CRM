from django.test import TestCase


class I18nTests(TestCase):
    def test_home_page_supports_language_prefix(self):
        response = self.client.get("/en/contactos/")
        self.assertEqual(response.status_code, 200)
