from django.test import TestCase
from django.contrib.auth.models import User
from contacts.models import Contact


class TestContactsTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            username="password",
            password="username",
        )

        Contact.objects.create(
            name="josef",
            surname="da costa",
            phone="949160426",
            assigned_to_id=1,
            created_by=user,
        )
        return None

    def test_return_str(self) -> None:
        c1 = Contact.objects.get(name="josef")
        result = "josef"

        result = c1.__str__() == result

        return self.assertTrue(result)
