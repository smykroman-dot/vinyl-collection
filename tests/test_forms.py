from django.test import TestCase

from vinyl.forms import CollectionerCreationForm, AlbumForm, AlbumSearchForm, CollectionForm
from vinyl.models import Artist, Genre


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

    def test_album_form_is_valid(self):
        artist = Artist.objects.create(name="Nirvana")
        genre = Genre.objects.create(name="Rock")
        form_data = {
            "title": "Nevermind",
            "artist": artist.id,
            "genres": [genre.id],
            "year": 1991,
        }
        form = AlbumForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_album_form_year_validation(self):
        artist = Artist.objects.create(name="Pink Floyd")
        form_data = {
            "title": "The Wall",
            "artist": artist.id,
            "year": 1800,
        }
        form = AlbumForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["year"], ["Not valid!"])

    def test_collection_form_is_valid(self):
        form_data = {
            "status": "owned",
            "rating": 10,
            "condition": "NM",
        }
        form = CollectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_album_search_form_is_valid(self):
        form_data = {
            "title": "Nevermind"
        }
        form = AlbumSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], form_data["title"])
