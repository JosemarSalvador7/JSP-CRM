from django.test import TestCase
from opportunities.forms import OpportunityForm
from django.contrib.auth.models import User
from contacts.models import Contact


class TestOpportunityForm(TestCase):
    def setUp(self) -> None:
        User.objects.create(username="password", password="username")
        
        Contact.objects.create(
            name="josef",
            surname="da costa",
            phone="949160426",
            assigned_to_id=1,
            created_by=User.objects.first(),
        )
        
        return super().setUp()

    def test_form_opportunities_if_is_valid(self):
        form = OpportunityForm(
            data={
                "name": "opportunities_test",
                "value": 20000,
                "stage": "PROSPECTING",
                "assigned_to": User.objects.get(id=1),
                "contact": Contact.objects.get(id=1),
            }
        )
        form_result = form.is_valid()
        return self.assertTrue(form_result, msg=f"{form.errors}")

    def test_form_opportunities_if_is_invalid(self):
        form = OpportunityForm(
            data={
                "name": "opportunities_test",
                "value": -20000,
                "stage": "PROSPECTING",
                "assigned_to": User.objects.get(id=1),
            }
        )
        form_result = form.is_valid()
        return self.assertFalse(form_result, msg=f'{form.errors}')
