from django.test import TestCase
from contacts.form import ContactForm
from django.contrib.auth.models import User


class TestContactForm(TestCase):
    def setUp(self) -> None:
        User.objects.create(username="password", password="username")
        return super().setUp()

    def test_form_contact_if_is_valid(self):
        form = ContactForm(
            data={
                "name": "josef",
                "surname": "da costa",
                "phone": "949160426",
                "assigned_to": User.objects.get(id=1),
            }
        )
        form_result = form.is_valid()
        return self.assertTrue(form_result, msg=f"{form.errors}")

    def test_form_contact_if_is_invalid(self):
        form = ContactForm(
            data={"name": "josef", "surname": "da costa", "phone": "949160426"}
        )
        form_result = form.is_valid()
        return self.assertFalse(form_result)
    
    def test_if_form_contact_accept_emogi(self):
        form = ContactForm(
            data={
                "name": "Armando🐍",
                "surname": "da costa",
                "phone": "949160426",
                "assigned_to": User.objects.get(id=1),
            }
        )
        form_result = form.is_valid()
        return self.assertFalse(form_result, msg=f"{form.errors}")
    
 