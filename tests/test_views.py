from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from vinyl.models import Genre, Artist, Album, Collection

GENRE_URL = reverse("vinyl:genre-list")
GENRE_LIST_URL = reverse("vinyl:genre-list")
GENRE_CREATE_URL = reverse("vinyl:genre-create")
ARTIST_LIST_URL = reverse("vinyl:artist-list")
ARTIST_CREATE_URL = reverse("vinyl:artist-create")
ALBUM_LIST_URL = reverse("vinyl:album-list")
ALBUM_CREATE_URL = reverse("vinyl:album-create")
MY_COLLECTION_URL = reverse("vinyl:my-collection")

class PublicGenreListViewTests(TestCase):

    def test_login_required(self):
        res = self.client.get(GENRE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateGenreListViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_genres(self):
        Genre.objects.create(name="Jazz")
        response = self.client.get(GENRE_URL)
        self.assertEqual(response.status_code, 200)
        genres = Genre.objects.all().order_by("name")
        self.assertEqual(
            list(response.context["genres"]),
            list(genres),
        )
        self.assertTemplateUsed(
            response,
            "vinyl/genre_list.html"
        )


class PublicArtistViewsTests(TestCase):

    def test_login_required_for_artist_list(self):
        response = self.client.get(ARTIST_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateArtistViewsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_artists(self):
        Artist.objects.create(name="Nirvana")
        Artist.objects.create(name="Pink Floyd")
        response = self.client.get(ARTIST_LIST_URL)
        artists = Artist.objects.all().order_by("name")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["artists"]),
            list(artists),
        )
        self.assertTemplateUsed(
            response,
            "vinyl/artist_list.html"
        )

    def test_create_artist(self):
        response = self.client.post(
            ARTIST_CREATE_URL,
            {
                "name": "Radiohead",
                "country": "UK",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Artist.objects.filter(name="Radiohead").exists()
        )

    def test_update_artist(self):
        artist = Artist.objects.create(
            name="Old Artist",
            country="USA"
        )
        response = self.client.post(
            reverse("vinyl:artist-update", args=[artist.id]),
            {
                "name": "New Artist",
                "country": "UK",
            }
        )
        artist.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(artist.name, "Old Artist")

    def test_delete_artist(self):
        artist = Artist.objects.create(name="Delete Artist")

        response = self.client.post(
            reverse("vinyl:artist-delete", args=[artist.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Artist.objects.filter(id=artist.id).exists()
        )

    def test_artist_detail(self):
        artist = Artist.objects.create(name="Queen")

        response = self.client.get(
            reverse("vinyl:artist-detail", args=[artist.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["artist"],
            artist
        )
        self.assertTemplateUsed(
            response,
            "vinyl/artist_detail.html"
        )


class PublicAlbumViewsTests(TestCase):
    def test_login_required_for_album_list(self):
        response = self.client.get(ALBUM_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAlbumViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_albums(self):
        artist = Artist.objects.create(name="Metallica")
        Album.objects.create(
            title="Black Album",
            artist=artist
        )
        response = self.client.get(ALBUM_LIST_URL)
        albums = Album.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["albums"]),
            list(albums),
        )
        self.assertTemplateUsed(
            response,
            "vinyl/album_list.html"
        )

    def test_search_album(self):
        artist = Artist.objects.create(name="Nirvana")
        Album.objects.create(
            title="Nevermind",
            artist=artist
        )
        Album.objects.create(
            title="In Utero",
            artist=artist
        )
        response = self.client.get(
            ALBUM_LIST_URL,
            {"title": "Never"}
        )
        self.assertContains(response, "Nevermind")
        self.assertNotContains(response, "In Utero")

    def test_create_album(self):
        artist = Artist.objects.create(name="Muse")
        response = self.client.post(
            ALBUM_CREATE_URL,
            {
                "title": "Absolution",
                "artist": artist.id,
                "year": 2003,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Album.objects.filter(title="Absolution").exists()
        )

    def test_update_album(self):
        artist = Artist.objects.create(name="Blur")
        album = Album.objects.create(
            title="Old",
            artist=artist
        )
        response = self.client.post(
            reverse("vinyl:album-update", args=[album.id]),
            {
                "title": "New",
                "artist": artist.id,
                "year": 1999,
            }
        )
        album.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(album.title, "New")

    def test_delete_album(self):
        artist = Artist.objects.create(name="Oasis")
        album = Album.objects.create(
            title="Definitely Maybe",
            artist=artist
        )
        response = self.client.post(
            reverse("vinyl:album-delete", args=[album.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Album.objects.filter(id=album.id).exists()
        )

    def test_album_detail(self):
        artist = Artist.objects.create(name="Coldplay")
        album = Album.objects.create(
            title="Parachutes",
            artist=artist
        )
        response = self.client.get(
            reverse("vinyl:album-detail", args=[album.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["album"],
            album
        )
        self.assertTemplateUsed(
            response,
            "vinyl/album_detail.html"
        )

    def test_album_detail(self):
        artist = Artist.objects.create(name="Coldplay")
        album = Album.objects.create(
            title="Parachutes",
            artist=artist,
            year=2000,
        )
        response = self.client.get(
            reverse("vinyl:album-detail", args=[album.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["album"],
            album
        )
        self.assertTemplateUsed(
            response,
            "vinyl/album_detail.html"
        )


class PrivateCollectionViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )
        self.client.force_login(self.user)

    def test_my_collection(self):
        artist = Artist.objects.create(name="Daft Punk")
        album = Album.objects.create(
            title="Discovery",
            artist=artist
        )
        Collection.objects.create(
            user=self.user,
            album=album,
            status="owned"
        )
        response = self.client.get(MY_COLLECTION_URL)
        items = Collection.objects.filter(user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["items"]),
            list(items),
        )
        self.assertTemplateUsed(
            response,
            "vinyl/my_collection.html"
        )

    def test_add_album_to_collection(self):
        artist = Artist.objects.create(name="ABBA")
        album = Album.objects.create(
            title="Gold",
            artist=artist
        )
        response = self.client.post(
            reverse("vinyl:collection-add", args=[album.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Collection.objects.filter(
                user=self.user,
                album=album
            ).exists()
        )

    def test_update_collection_item(self):
        artist = Artist.objects.create(name="Korn")
        album = Album.objects.create(
            title="Issues",
            artist=artist
        )
        item = Collection.objects.create(
            user=self.user,
            album=album,
            status="owned"
        )
        response = self.client.post(
            reverse("vinyl:collection-update", args=[item.id]),
            {
                "status": "wishlist",
                "rating": 9,
                "condition": "NM",
            }
        )
        item.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(item.status, "wishlist")

    def test_delete_collection_item(self):
        artist = Artist.objects.create(name="Slayer")

        album = Album.objects.create(
            title="Reign in Blood",
            artist=artist
        )
        item = Collection.objects.create(
            user=self.user,
            album=album,
        )
        response = self.client.post(
            reverse("vinyl:collection-delete", args=[item.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Collection.objects.filter(id=item.id).exists()
        )
