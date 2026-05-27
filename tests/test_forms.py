from django.test import TestCase

from vinyl.forms import CollectionerCreationForm


class FormsTests(TestCase):

    def test_collectioner_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "userpassword12",
            "password2": "userpassword12",
            "first_name": "John",
            "last_name": "BonJovi",
            "country": "Ukraine",
        }

        form = CollectionerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(form.cleaned_data["country"], form_data["country"])