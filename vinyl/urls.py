from django.urls import path
from .views import (
    index,
    GenreListView,
    GenreCreateView,
    GenreUpdateView,
    GenreDeleteView,
    ArtistListView,
    ArtistCreateView,
    ArtistUpdateView,
    ArtistDeleteView,
    ArtistDetailView,
    AlbumListView,
    AlbumCreateView,
    AlbumUpdateView,
    AlbumDeleteView,
    AlbumDetailView,
    AlbumByYearView,
    UsersCreateView,
    MyCollectionView,
    CollectionAddView,
    CollectionUpdateView,
    CollectionDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/create/", GenreCreateView.as_view(), name="genre-create"),
    path("genres/<int:pk>/update/", GenreUpdateView.as_view(), name="genre-update"),
    path("genres/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre-delete"),

    path("artists/", ArtistListView.as_view(), name="artist-list"),
    path("artists/create/", ArtistCreateView.as_view(), name="artist-create"),
    path("artists/<int:pk>/update/", ArtistUpdateView.as_view(), name="artist-update"),
    path("artists/<int:pk>/delete/", ArtistDeleteView.as_view(), name="artist-delete"),
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name="artist-detail"),

    path("albums/", AlbumListView.as_view(), name="album-list"),
    path("albums/create/", AlbumCreateView.as_view(), name="album-create"),
    path("albums/<int:pk>/update/", AlbumUpdateView.as_view(), name="album-update"),
    path("albums/<int:pk>/delete/", AlbumDeleteView.as_view(), name="album-delete"),
    path("albums/<int:pk>/", AlbumDetailView.as_view(), name="album-detail"),
    path("albums/year/<int:year>/", AlbumByYearView.as_view(), name="album-by-year"),

    path("users/create/", UsersCreateView.as_view(), name="user-create"),

    path("albums/<int:pk>/add-to-collection/", CollectionAddView.as_view(), name="collection-add"),
    path("collection/<int:pk>/update/", CollectionUpdateView.as_view(), name="collection-update"),
    path("collection/<int:pk>/delete/", CollectionDeleteView.as_view(), name="collection-delete"),

    path("my-collection/", MyCollectionView.as_view(), name="my-collection"),

]

app_name = "vinyl"
