import os
import django
import requests

from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vinylcollection.settings")
django.setup()

from vinyl.models import Album
from vinyl.utils.seed_albums import get_cover


albums = [
    (20, "AC/DC", "Back in Black"),
    (21, "Pink Floyd", "The Dark Side of the Moon"),
    (22, "Nirvana", "Nevermind"),
    (23, "Michael Jackson", "Thriller"),
    (24, "Fleetwood Mac", "Rumours"),
    (25, "Pink Floyd", "The Wall"),
    (26, "Guns N' Roses", "Appetite for Destruction"),
    (27, "Eagles", "Hotel California"),
    (28, "Adele", "21"),
    (29, "Radiohead", "OK Computer"),
]

for album_id, artist, title in albums:
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        print("Not found:", album_id)
        continue

    url = get_cover(artist, title)

    if not url:
        print("No cover:", title)
        continue

    response = requests.get(url)

    if response.status_code == 200:
        album.cover.save(
            f"{album_id}.jpg",
            ContentFile(response.content),
            save=True
        )
        print("Saved:", title)