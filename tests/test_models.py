from django.contrib.auth import get_user_model
from django.test import TestCase

from vinyl.models import Artist, Genre, Album, Collection


class ModelsTests(TestCase):

    def test_artist_str(self):
        artist = Artist.objects.create(name="Pink Floyd", country="UK")
        self.assertEqual(str(artist), "Pink Floyd")

    def test_genre_str(self):
        genre = Genre.objects.create(name="Rock")
        self.assertEqual(str(genre), "Rock")

    def test_album_str(self):
        artist = Artist.objects.create(name="Pink Floyd", country="UK")
        album = Album.objects.create(
            title="Nevermind",
            artist=artist
        )
        self.assertEqual(str(album), "Pink Floyd - Nevermind")

    def test_collection_str(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="pass123"
        )
        artist = Artist.objects.create(
            name="Nirvana"
        )
        album = Album.objects.create(
            title="Nevermind",
            artist=artist
        )
        collection = Collection.objects.create(
            user=user,
            album=album,
            status="owned"
        )
        self.assertEqual(
            str(collection),
            "testuser - Nevermind (Owned)"
        )

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            password="password",
            first_name="John",
            last_name="BonJovi",
            country="Ukraine"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "BonJovi")
        self.assertEqual(user.country, "Ukraine")
        self.assertTrue(user.check_password("password"))
