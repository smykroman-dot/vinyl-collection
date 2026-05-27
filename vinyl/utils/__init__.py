from django.core.management.base import BaseCommand
from vinyl.models import Album, Artist


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        albums_data = [
            (20, "Back in Black", "AC/DC", 1980),
            (21, "The Dark Side of the Moon", "Pink Floyd", 1973),
            (22, "Nevermind", "Nirvana", 1991),
            (23, "Thriller", "Michael Jackson", 1982),
            (24, "Rumours", "Fleetwood Mac", 1977),
            (25, "The Wall", "Pink Floyd", 1979),
            (26, "Appetite for Destruction", "Guns N' Roses", 1987),
            (27, "Hotel California", "Eagles", 1976),
            (28, "21", "Adele", 2011),
            (29, "OK Computer", "Radiohead", 1997),
        ]

        for pk, title, artist_name, year in albums_data:
            artist = Artist.objects.get(name=artist_name)

            album, created = Album.objects.get_or_create(
                id=pk,
                defaults={
                    "title": title,
                    "artist": artist,
                    "year": year,
                }
            )

            self.stdout.write(f"{title} -> {created}")